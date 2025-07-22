from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load tokenizer and model from local path (e.g., Google Drive)
drive_model_path = "/content/drive/MyDrive/mistral_model"

tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(
    drive_model_path,
    device_map="auto",
    torch_dtype=torch.float16
)

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Prompt formatting function with match info and score
def format_prompt(event, context, match_context, current_score):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].replace("_", " ").capitalize()

# Updated Prompt Template with Example

    prompt = f"""
    1) You are a football commentator.

    2) Your job is to generate exciting and vivid real-time football commentary based on:
    - The current match event
    - The player involved
    - The player's key stats from last season
    - The match being played
    - The current score

    3) Use dynamic, natural language.

    4) Describe the event in an entertaining way, as if you were commentating live on TV.

    5) Focus on the player's most relevant stats from last season, such as goals, assists, red cards, yellow cards, and minutes played.

    6) Do not say things out of context; only use the information provided.

    7) You will be given the following information:

    ### Match:
    - Arsenal vs Manchester City
    - Current Score: 1-0
    - Starting Lineup: 
    Arsenal: Ramsdale, White, Saliba, Gabriel, Zinchenko, Rice, Ødegaard, Havertz, Saka, Martinelli, Gabriel Jesus
    Manchester City: Ederson, Walker, Aké, Dias, Gvardiol, Rodri, Bernardo, De Bruyne, Foden, Doku, Haaland

    ### Event:
    - Minute: 32
    - Type: Goal
    - Player: Gabriel Jesus

    ### Player key Stats from last season:
    {{ 
        "position": "FWD",
        "goals": 3,
        "assists": 2,
        "minutes_played": 600,
        "yellow_cards": 4,
        "red_cards": 0
    }}
    
    ### Example:
    32' – It's Gabriel Jesus with the breakthrough! The Brazilian striker finds a pocket of space inside the box and lashes it past Ederson!  
    That’s his third goal of the season, and what a moment to get it against his former club! With 600 minutes played and 2 assists last season,  
    he's proving his worth up front again. Arsenal takes the lead, 1–0!

    ### Commentary:
    """

    return prompt.strip()

# Example input
match_context = "Arsenal vs Manchester City"
current_score = "1-1"
event = {"minute": "47", "type": "assist", "player": "Kevin De Bruyne"}
context = {
    "name": "Kevin De Bruyne",
    "position": "MID",
    "goals": 5,
    "assists": 16,
    "minutes_played": 2100,
    "yellow_cards": 2,
    "red_cards": 0,
    "lineup": {
        "Arsenal": [
            "Ramsdale", "White", "Saliba", "Gabriel", "Zinchenko",
            "Rice", "Ødegaard", "Havertz", "Saka", "Martinelli", "Gabriel Jesus"
        ],
        "Manchester City": [
            "Ederson", "Walker", "Aké", "Dias", "Gvardiol",
            "Rodri", "Bernardo", "De Bruyne", "Foden", "Doku", "Haaland"
        ]
    }
}

# Build and tokenize prompt
prompt = format_prompt(event, context, match_context, current_score)
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate model output
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=150,
    do_sample=True,
    top_p=0.9,
    temperature=0.8,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id,
)

# Decode and extract commentary
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
if "Commentary:" in generated_text:
    print("\n🎙️ Commentary:")
    print(generated_text.split("Commentary:")[1].strip())
else:
    print(generated_text)

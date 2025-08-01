from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

def trim_to_last_complete_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return " ".join(sentences[:-1]) if len(sentences) > 1 else text



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
def build_prompt_with_example(home_team, away_team, current_score, lineup, event, context):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].capitalize()

    prompt = f"""
You are a live football commentator.

Your task is to generate **EXCITING, VIVID, REAL-TIME COMMENTARY** for the following single football event.  
ONLY use the information provided below — DO NOT guess or invent anything.

RULES (follow strictly):
- Use natural, energetic commentary style.
- You MUST mention the event minute clearly in the commentary.
- Only describe the event, not the whole match.
- DO NOT mention:
  - Player nationality
  - Club history
  - Player backstory
  - Anything not given explicitly
- Only include STATS from last season if they are non-zero.
- DO NOT mention zero stats or make assumptions.
- Always use the player's and team's name as given in the context.

--- MATCH INFO ---
Match: {home_team} vs {away_team}
Current Score: {current_score}  
Starting Lineup:  
{lineup}

--- EVENT INFO ---
Minute: {minute}  
Event Type: {event_type}  
Player: {player}

--- {player} STATS LAST SEASON ---
Position: {context.get("position", "N/A")}  
Goals: {context.get("goals", 0)}  
Assists: {context.get("assists", 0)}  
Minutes Played: {context.get("minutes_played", 0)}  
Yellow Cards: {context.get("yellow_cards", 0)}  
Red Cards: {context.get("red_cards", 0)}

--- EXAMPLE FORMAT ---
"{player} surges down the right wing and whips in a cross! With {context.get("goals", 0)} and {context.get("assists", 0)} last season, he's always a danger man in these situations."
"{player} doas a bad tackle and receives a yellow card! Last season, he had {context.get("yellow_cards", 0)} yellow cards and {context.get("red_cards", 0)} red cards, he's known for having good discipline on the pitch."

--- COMMENTARY ---
Minute {minute}:
"""

    return prompt.strip()

# Primo evento (esempio fisso)
example_commentary = (
    "32' – It's Gabriel Jesus with the breakthrough! The Brazilian striker finds a pocket of space inside the box and lashes it past Ederson! "
    "That’s his third goal of the season, and what a moment to get it against his former club! With 600 minutes played and 2 assists last season, "
    "he's proving his worth up front again. Arsenal takes the lead, 1–0!"
)

# Nuovo evento (per testare il modello senza fornire un nuovo esempio)
new_event = {"minute": 45, "type": "yellow_card", "player": "Romelu Lukaku"}
new_context = {
    "name": "Romelu Lukaku",
    "position": "MID",
    "goals": 5,
    "assists": 7,
    "minutes_played": 1100,
    "yellow_cards": 2,
    "red_cards": 0
}

prompt = build_prompt_with_example(
    home_team="Arsenal",
    away_team="Manchester City",
    current_score="1-0",
    lineup=(
        "Arsenal: Ramsdale, White, Saliba, Gabriel, Zinchenko, Rice, Ødegaard, Havertz, Saka, Martinelli, Gabriel Jesus\n"
        "Manchester City: Ederson, Walker, Aké, Dias, Gvardiol, Rodri, Bernardo, De Bruyne, Foden, Doku, Haaland"
    ),
    event=new_event,
    context=new_context,)

# Passa prompt al modello e genera output
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=150,
    do_sample=True,
    top_p=0.85,
    temperature=0.7,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id,
)

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
if "Commentary:" in generated_text:
    commentary = generated_text.split("Commentary:")[1].strip()
    commentary = trim_to_last_complete_sentence(commentary)

else:
    commentary = generated_text
    commentary = trim_to_last_complete_sentence(commentary)


print("\n🎙️ Commentary for new event:")
print(commentary)

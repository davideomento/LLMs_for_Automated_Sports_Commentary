from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load tokenizer and model from local path (e.g., Google Drive)
drive_model_path = "/content/drive/MyDrive/mistral_model"

tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(drive_model_path, device_map="auto")

# Ensure model is in evaluation mode
model.eval()

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to format the input prompt for the model
def format_prompt(event, context):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].replace("_", " ").capitalize()

    # Base event description
    base = f"Minute {minute}': {event_type} involving {player}.\n\n"

    # Player statistics
    stats = (
        f"{player} has scored {context['goals']} goals and provided {context['assists']} assists this season. "
        f"He have played {context['minutes_played']} minutes, with an influence score of {context['influence']}, "
        f"threat of {context['threat']}, and creativity of {context['creativity']}.\n\n"
    )

    # Instruction with input/output examples
    instruction = (
        "You are a football commentator.\n"
        "Your job is to generate an exciting and natural-sounding commentary based on real-time match events and player statistics.\n"
        "Mention the minute, player name, and describe the action vividly.\n\n"
        "### Example Input:\n"
        "Minute 45': Goal involving Erling Haaland.\n\n"
        "Erling Haaland has scored 10 goals and provided 2 assists this season. "
        "He have played 980 minutes, with an influence score of 320.5, threat of 500.0, and creativity of 90.2.\n\n"
        "### Example Output:\n"
        "45' – It's Erling Haaland again! A powerful run through the center, and he buries it into the bottom corner! "
        "Ten goals this season and counting – what a force he's been for City!\n\n"
        "### Now continue with the following:\n\n"
    )

    return instruction + base + stats + "Commentary:\n"

# Example input
event = {"minute": "67", "type": "goal", "player": "Gabriel Jesus"}
context = {
    "name": "Gabriel Jesus",
    "position": "FWD",
    "goals": 3,
    "assists": 2,
    "minutes_played": 600,
    "goals_conceded": 5,
    "clean_sheets": 2,
    "yellow_cards": 4,
    "red_cards": 0,
    "influence": 154.4,
    "threat": 255.0,
    "creativity": 119.5,
    "total_points": 42
}

# Build the prompt
prompt = format_prompt(event, context)

# Tokenize the input prompt
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

# Decode and print the generated commentary
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Optional: Only print the part after "Commentary:"
if "Commentary:" in generated_text:
    print("\n🎙️ Commentary:")
    print(generated_text.split("Commentary:")[1].strip())
else:
    print(generated_text)

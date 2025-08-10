from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Format the prompt (same as your original structure)
def format_prompt(event, context):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].replace("_", " ").capitalize()

    base = f"Minute {minute}': {event_type} involving {player}.\n"
    stats = (
        f"{player} has scored {context['goals']} goals and provided {context['assists']} assists this season. "
        f"He's played {context['minutes_played']} minutes and shows an influence score of {context['influence']}, "
        f"threat of {context['threat']}, and creativity of {context['creativity']}."
    )

    instruction = (
        "\nYou are a football commentator tasked with generating a realistic commentary for a match event. "
        "You are given the player's stats and the event details and you have to tell as a commntator would do these events. "
        "Write an exciting and realistic football commentary based on this event and context. "
        "Mention the minute and player's name clearly."
        
    )

    return base + stats + instruction

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

# Load GPT-2 locally
model_name = "gpt2"  # You could also try "gpt2-medium" if you want slightly better performance
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Tokenize input prompt
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate output
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],  # Add this
    max_length=200,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9,
    pad_token_id=tokenizer.eos_token_id  # Add this
)


# Decode and print the generated commentary
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)

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
def build_prompt_with_example(match_context, current_score, lineup, event, context, example_commentary):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].capitalize()

    prompt = f"""
1) You are a football commentator.

2) Your job is to generate exciting and vivid real-time football commentary based strictly on the provided data:

- Match context, current score, lineup
- The current event: minute, type, player
- The player’s last season key stats (goals, assists, cards, minutes played)

3) IMPORTANT: Do NOT invent or add any details beyond the given data.  
Do NOT mention player nationality, club history, or any personal stories unless explicitly provided.  
Do NOT mention stats that are zero or missing.

4) Use dynamic, natural language to describe only the current event.

4.1) Always mention the minute of the event in the commentary to give a sense of live timing.

5) Commentary must only reflect the provided data, no hallucinations or invented details.

### Match:
- {match_context}
- Current Score: {current_score}
- Starting Lineup: 
{lineup}

### Event:
- Minute: {minute}
- Type: {event_type}
- Player: {player}

### Player key Stats from last season:
{{
    "position": "{context.get("position", "N/A")}",
    "goals": {context.get("goals", 0)},
    "assists": {context.get("assists", 0)},
    "minutes_played": {context.get("minutes_played", 0)},
    "yellow_cards": {context.get("yellow_cards", 0)},
    "red_cards": {context.get("red_cards", 0)}
}}

### Commentary:
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
new_event = {"minute": 45, "type": "yellow_card", "player": "Martin Ødegaard"}
new_context = {
    "name": "Martin Ødegaard",
    "position": "MID",
    "goals": 5,
    "assists": 7,
    "minutes_played": 1100,
    "yellow_cards": 2,
    "red_cards": 0
}

prompt = build_prompt_with_example(
    match_context="Arsenal vs Manchester City",
    current_score="1-0",
    lineup=(
        "Arsenal: Ramsdale, White, Saliba, Gabriel, Zinchenko, Rice, Ødegaard, Havertz, Saka, Martinelli, Gabriel Jesus\n"
        "Manchester City: Ederson, Walker, Aké, Dias, Gvardiol, Rodri, Bernardo, De Bruyne, Foden, Doku, Haaland"
    ),
    event=new_event,
    context=new_context,
    example_commentary=example_commentary
)

# Passa prompt al modello e genera output
inputs = tokenizer(prompt, return_tensors="pt").to(device)
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

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
if "Commentary:" in generated_text:
    commentary = generated_text.split("Commentary:")[1].strip()
else:
    commentary = generated_text

print("\n🎙️ Commentary for new event:")
print(commentary)

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

def build_prompt_goals(home_team, away_team, current_score, lineup, event, context):
    player = context["name"]
    minute = event["minute"]

    prompt = f"""
You are a live football commentator.

Generate ONE EXCITING and VIVID real-time commentary sentence describing a GOAL scored in a football match.

RULES:
- Mention the event minute, player name, and updated current score clearly.
- Use only the provided information. No guessing or extra details.
- Include last season stats ONLY if non-zero.
- Do NOT mention nationality, history, or player backstory.

--- EXAMPLES (with placeholders) ---

"Minute *minute* — What a fantastic strike from *player*! He brings the score to *current_score*. The crowd erupts as *home_team* take the lead!"

"GOAL at *minute*! *player* makes no mistake, slotting it past the keeper! With *goals* goals last season, he’s proving once again to be a key attacking threat. The scoreboard now reads *current_score*."

"*player* finishes brilliantly at *minute* after a superb buildup, delivering the decisive touch. Having scored *goals* goals and provided *assists* assists last season, he’s proving to be a key player once again. The score is now *current_score* — what a moment for *home_team*!

--- NOW USE THE DATA BELOW TO GENERATE COMMENTARY ---

Match: {home_team} vs {away_team}  
Current Score: {current_score}  
Starting Lineup:  
{lineup}

Event Minute: {minute}  
Scorer: {player}

{player} Stats Last Season:  
Position: {context.get("position", "N/A")}  
Goals: {context.get("goals", 0)}  
Assists: {context.get("assists", 0)}  
Minutes Played: {context.get("minutes_played", 0)}  
Yellow Cards: {context.get("yellow_cards", 0)}  
Red Cards: {context.get("red_cards", 0)}

--- COMMENTARY ---
"""
    return prompt.strip()

'''def build_prompt_goals(home_team, away_team, current_score, lineup, event, context):
    player = context["name"]
    minute = event["minute"]

    prompt = f"""
You are a live football commentator.

Your task is to generate **EXCITING, VIVID, REAL-TIME COMMENTARY** describing a GOAL scored in a football match.  
ONLY use the information provided below — DO NOT guess or invent anything.

RULES (follow strictly):
- Use natural, energetic commentary style full of enthusiasm.
- You MUST clearly mention the event minute, the player scoring the goal, and the updated current score.
- Only describe the goal event itself, not the entire match.
- DO NOT mention:
  - Player nationality
  - Club history
  - Player backstory
  - Anything not explicitly provided
- Only include STATS from last season if they are non-zero.
- DO NOT mention zero stats or make assumptions.
- Always use the player's and team's name exactly as given in the context.

--- MATCH INFO ---
Match: *home_team* vs *away_team*
Current Score: *current_score*  
Starting Lineup:  
*lineup*

--- EVENT INFO ---
Minute: *minute*  
Player: *player*

--- *player* STATS LAST SEASON ---
Position: *position*  
Goals: *goals*  
Assists: *assists*  
Minutes Played: *minutes_played*  
Yellow Cards: *yellow_cards*  
Red Cards: *red_cards*

--- EXAMPLE COMMENTARY ---

"Minute *minute* — What a fantastic strike from *player*! He brings the score to *current_score*. The crowd erupts as *home_team* take the lead!"

"GOAL at *minute*! *player* makes no mistake, slotting it past the keeper! With *goals* goals last season, he’s proving to be a key attacking threat. The scoreboard now reads *current_score*."

"*player* finishes brilliantly at *minute* after a superb buildup, delivering the decisive touch. Having scored *goals* goals and provided *assists* assists last season, he’s proving to be a key player once again. The score is now *current_score* — what a moment for *home_team*!"

--- NOW USE THE REAL DATA BELOW TO GENERATE COMMENTARY ---

--- MATCH INFO ---
Match: {home_team} vs {away_team}
Current Score: {current_score}  
Starting Lineup:  
{lineup}

--- EVENT INFO ---
Minute: {minute}  
Player: {player}

--- {player} STATS LAST SEASON ---
Position: {context.get("position", "N/A")}  
Goals: {context.get("goals", 0)}  
Assists: {context.get("assists", 0)}  
Minutes Played: {context.get("minutes_played", 0)}  
Yellow Cards: {context.get("yellow_cards", 0)}  
Red Cards: {context.get("red_cards", 0)}

Generate ONE vivid commentary sentence for this goal event, using ONLY the info below.

--- COMMENTARY ---
"""

    return prompt.strip()'''


# Nuovo evento (per testare il modello senza fornire un nuovo esempio)
new_event = {"minute": 45, "type": "yellow_card", "player": "Gabriel Jesus"}
new_context = {
    "name": "Gabriel Jesus",
    "position": "STRIKER",
    "goals": 5,
    "assists": 7,
    "minutes_played": 1100,
    "yellow_cards": 2,
    "red_cards": 0
}

prompt = build_prompt_goals(
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

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

def trim_to_last_complete_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if sentences and re.match(r'.*[.!?]$', sentences[-1]):
        # L'ultima frase è completa, restituisci tutto
        return text
    elif len(sentences) > 1:
        # Taglia l'ultima frase incompleta
        return " ".join(sentences[:-1])
    else:
        return text


# Load tokenizer and model from local path (e.g., Google Drive)
drive_model_path = "/content/drive/MyDrive/mistral_model"

tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(
    drive_model_path,
    device_map="auto",
    torch_dtype=torch.float16
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.eval()


def build_prompt_goals(home_team, away_team, current_score, lineup, event, context):
    player = event.get("player", context.get("name", "Unknown"))
    minute = event["minute"]

    goals = context.get("goals", 0)
    assists = context.get("assists", 0)
    position = context.get("position", "N/A")
    yellow_cards = context.get("yellow_cards", 0)
    red_cards = context.get("red_cards", 0)

    prompt = f"""
You are a live football commentator.

Generate ONE EXCITING and VIVID real-time commentary sentence describing a GOAL scored in a football match.

RULES:
- Use ONLY the exact data provided below.
- Do NOT invent, guess, or approximate any information.
- Do NOT mention statistics or details not provided.
- If a stat is zero or missing, do NOT mention it.
- Mention the exact event minute and current score as given.
- Use all names exactly as provided without modification.
- Your sentence should be a single, extended commentary sentence.
- Include relevant last season statistics naturally to enrich the commentary.
- Generate ONE sentence only, using exactly these placeholders: EVENT_MINUTE, SCORER, CURRENT_SCORE, LAST_SEASON_GOALS, LAST_SEASON_ASSISTS.
- Do NOT add or invent any other information.

Use the data below to generate commentary:

Match: {home_team} vs {away_team}  
Current Score: {current_score}  
Starting Lineup:  
{lineup}

Event Minute: {minute}  
Scorer: {player}

{player} Stats Last Season:  
Position: {position}  
Goals: {goals}  
Assists: {assists}  
Yellow Cards: {yellow_cards}  
Red Cards: {red_cards}

COMMENTARY:
"""
    return prompt.strip()


# Dati esempio evento e contesto
new_event = {"minute": 45, "type": "goal", "player": "Gabriel Jesus"}
new_context = {
    "name": "Gabriel Jesus",
    "position": "STRIKER",
    "goals": 5,
    "assists": 7,
    "minutes_played": 1100,
    "yellow_cards": 2,
    "red_cards": 0
}

lineup_text = (
    "Arsenal: Ramsdale, White, Saliba, Gabriel, Zinchenko, Rice, Ødegaard, Havertz, Saka, Martinelli, Gabriel Jesus\n"
    "Manchester City: Ederson, Walker, Aké, Dias, Gvardiol, Rodri, Bernardo, De Bruyne, Foden, Doku, Haaland"
)

prompt = build_prompt_goals(
    home_team="Arsenal",
    away_team="Manchester City",
    current_score="1-0",
    lineup=lineup_text,
    event=new_event,
    context=new_context
)

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

if "COMMENTARY:" in generated_text:
    commentary = generated_text.split("COMMENTARY:")[1].strip()
    commentary = trim_to_last_complete_sentence(commentary)
else:
    commentary = trim_to_last_complete_sentence(generated_text)

print("\n🎙️ Commentary for new event:")
print(commentary)

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

    # Filtra statistiche (no zeri o nulli)
    stats_parts = []
    if context.get("position"):
        stats_parts.append(f"Position: {context['position']}")
    if context.get("goals", 0) > 0:
        stats_parts.append(f"Goals: {context['goals']}")
    if context.get("assists", 0) > 0:
        stats_parts.append(f"Assists: {context['assists']}")
    if context.get("minutes_played", 0) > 0:
        stats_parts.append(f"Minutes Played: {context['minutes_played']}")
    if context.get("yellow_cards", 0) > 0:
        stats_parts.append(f"Yellow Cards: {context['yellow_cards']}")
    if context.get("red_cards", 0) > 0:
        stats_parts.append(f"Red Cards: {context['red_cards']}")
    stats_block = "\n".join(stats_parts)

    prompt = f"""TASK:
You are a live football commentator. 
Generate ONE EXCITING and VIVID real-time commentary sentence describing a GOAL scored in a football match.
---
STRICT RULES:
- Use ONLY the exact data provided below.
- Do NOT invent, guess, or add any context such as how the goal was scored, player movements, or match events not listed.
- If a statistic is zero or missing, do NOT mention it.
- Mention the exact event minute and current score as given.
- Use all names exactly as provided without modification.
- Your sentence must be a single, extended commentary sentence.
- Any additional detail must come ONLY from the provided last season statistics.
- Excitement should come from expressive wording, not fabricated match events.
---

EXAMPLE 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
SCORER Stats Last Season:
Position: POSITION
Goals: 12
Assists: 5

OUTPUT:
"GOAL at EVENT_MINUTE! SCORER finds the net again — with 12 goals and 5 assists last season, he’s showing why he’s a key man for HOME_TEAM. The score is now CURRENT_SCORE."
---

EXAMPLE 2:
INPUT:
Match: Chelsea vs Manchester United
Current Score: 2-1
Event Minute: 45
Scorer: Cole Palmer
SCORER Stats Last Season:
Position: MIDFIELDER
Goals: 10
Assists: 15
Minutes Played: 1648
Yellow Cards: 4

OUTPUT:
"Minute 45 — Cole Palmer fires it home! With 10 goals and 15 assists last season, he's proving his worth. Chelsea now lead 2-1."
---

=== NOW GENERATE ===
INPUT:
Match: {home_team} vs {away_team}
Current Score: {current_score}
Event Minute: {minute}
Scorer: {player}
{player} Stats Last Season:
{stats_block}

OUTPUT:"""

    return prompt




new_event = {"minute": 36, "type": "goal", "player": "Gabriel Jesus"}
new_context = {
    "name": "Gabriel Jesus",
    "position": "STRIKER",
    "goals": 60,
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

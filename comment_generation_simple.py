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

def build_prompt(home_team, away_team, current_score, event, context):
    player = context["name"]
    minute = event["minute"]
    event_type = event.get("type", "").lower()

    stats_parts = []

    position = context.get("position", "N/A")
    stats_parts.append(f"Position: {position}")

    goals = context.get("goals", 0)
    stats_parts.append(f"Goals: {goals}")

    assists = context.get("assists", 0)
    stats_parts.append(f"Assists: {assists}")

    minutes_played = context.get("minutes_played", 0)
    stats_parts.append(f"Minutes Played: {minutes_played}")

    yellow_cards = context.get("yellow_cards", 0)
    stats_parts.append(f"Yellow Cards: {yellow_cards}")

    red_cards = context.get("red_cards", 0)
    stats_parts.append(f"Red Cards: {red_cards}")

    stats_block = "\n".join(stats_parts)
    # GOAL
    if event_type == "goal":
        prompt = f"""TASK:
Act as a live football commentator. Using only the provided match data, create a vivid,
energetic, and natural-sounding single-sentence commentary describing the moment a goal is scored.
---
---

STRICT RULES:
- Use ONLY the exact data provided below.
- Do NOT invent, guess, or add any context such as how the goal was scored, player movements, or match events not listed.
- If a statistic is missing, do NOT mention it.
- Mention the exact event minute and current score as given.
- Use all names exactly as provided without modification.

EXAMPLE 1(anonymous):
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
SCORER Stats This Season:
Position: POSITION
Goals: 12
Assists: 5

OUTPUT:
"GOAL at EVENT_MINUTE! SCORER finds the net again — with 12 goals and 5 assists this season, he’s showing why he’s a key man for HOME_TEAM. The score is now CURRENT_SCORE."
---

EXAMPLE 2(anonymous):
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
SCORER Stats This Season:
Position: POSITION
Goals: GOALS
Assists: ASSISTS

OUTPUT:
"Minute EVENT_MINUTE — SCORER strikes again! With GOALS goals and ASSISTS assists this season, they continue to be a key player for HOME_TEAM. The score is now CURRENT_SCORE.
---

EXAMPLE 3(anonymous):
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
SCORER Stats This Season:
Position: DEFENDER
Goals: 0
Assists: 3

OUTPUT:
"Minute EVENT_MINUTE — SCORER scores a rare goal! Despite scoring 0 goals and providing 3 assists this season, its contribution remains crucial. The score is now CURRENT_SCORE."
---

EXAMPLE 4(real data):
INPUT:
Match: LIVERPOOL vs EVERTON
Current Score: 3-2
Event Minute: 78
Scorer: Mohamed Salah
SCORER Stats This Season:
Position: FORWARD
Goals: 22
Assists: 8

OUTPUT:
"Minute 78 — Mohamed Salah strikes again! With 22 goals and 8 assists this season, he continues to be Liverpool’s attacking powerhouse. The score is now 3-2."

---

=== NOW GENERATE USING THE FOLLOWING DATA ===

INPUT:
Match: {home_team} vs {away_team}
Current Score: {current_score}
Event Minute: {minute}
Scorer: {player}
{player} Stats This Season:
{stats_block}

OUTPUT:"""
        

    # YELLOW CARD
    elif event_type == "yellow_card":
        prompt = f"""TASK
Act as a live football commentator. Using only the provided match data, create a vivid, energetic, and natural-sounding single-sentence commentary describing the moment a player gets a yellow card.

STRICT RULES
- Use only the exact data provided.
- Do not invent, guess, or add any extra context.
- If a statistic is missing, do not mention it.
- Mention the exact event minute.
- Use all names exactly as provided without modification.

Example 1
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player: PLAYER
PLAYER Stats This Season:
Position: POSITION
Goals: GOALS
Assists: ASSISTS
Yellow Cards: YELLOW_CARDS

OUTPUT:
"Minute EVENT_MINUTE — PLAYER is shown his YELLOW_CARDS yellow card of the season. A tough blow for AWAY_TEAM, who trail CURRENT_SCORE.

NOW GENERATE USING THE FOLLOWING DATA

Match: {home_team} vs {away_team}
Current Score: {current_score}
Event Minute: {minute}
Scorer: {player}
{player} Stats This Season:
{stats_block}
"""
    else:
        # Default fallback prompt (can be extended for other event types)
        prompt = f"""TASK:
You are a live football commentator. Generate a lively commentary sentence using only the provided data.
---
INPUT:
Match: {home_team} vs {away_team}
Current Score: {current_score}
Event Minute: {minute}
Player: {player}
{player} Stats This Season:
{stats_block}

OUTPUT:"""

    return prompt.strip()





new_event = {"minute": 36, "type": "goal", "player": "Gabriel Jesus"}
new_context = {
    "name": "Gabriel Jesus",
    "position": "STRIKER",
    "goals": 10,
    "assists": 12,
    "minutes_played": 1100,
    "yellow_cards": 2,
    "red_cards": 0
}

prompt = build_prompt(
    home_team="Arsenal",
    away_team="Manchester City",
    current_score="1-0",
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




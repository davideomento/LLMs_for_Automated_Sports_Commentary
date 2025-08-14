'''from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
'''
'''def trim_to_last_complete_sentence(text):
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
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")'''


def prompt_goal(home_team, away_team, current_score, minute, scorer, assist, goal_type, shot_position, player_info, player_stats, player_achievements, team_profile_away, team_profile_home):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a vivid,
energetic, and natural-sounding single-sentence commentary describing the moment a goal is scored.

STRICT RULES:
- Use ONLY the exact data provided below.
- Do NOT invent, guess, or add any context such as how the goal was scored, player movements, or match events not listed.
- If a statistic is missing, do NOT mention it.
- Mention the exact event minute and current score as given.
- Use all names exactly as provided without modification.

EXAMPLE 1 :
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
Assister: ASSISTER
Goal Type: GOAL_TYPE
Shot Position: SHOT_POSITION
Scorer Goals this Season: GOALS
Scorer Assists this Season: ASSISTS

OUTPUT:
"GOAL at EVENT_MINUTE! SCORER finds the net from SHOT_POSITION — with GOALS goals and ASSISTS assists this season, 
he's proving to be a key man for HOME_TEAM. The score is now CURRENT_SCORE. Credit goes to ASSISTER for the assist.
---

EXAMPLE 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
Assister: ASSISTER
Goal Type: GOAL_TYPE
Shot Position: SHOT_POSITION
Scorer Age: AGE
Matches Played this Season: MATCHES_PLAYED

OUTPUT:
"Minute EVENT_MINUTE — SCORER scores from SHOT_POSITION with a brilliant GOAL_TYPE finish! 
At AGE years old and with MATCHES_PLAYED appearances this season, he's showing incredible form for HOME_TEAM. 
The score is now CURRENT_SCORE, thanks to a precise assist from ASSISTER."

---

INPUT:
Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Scorer: {scorer}
Assist: {assist}
Goal Type: {goal_type}
Position of the shot: {shot_position}
{scorer} Info: {player_info}
{scorer} Stats: {player_stats}
{scorer} Achievements: {player_achievements}


OUTPUT:"""

def prompt_attempted_shot(home_team, away_team, current_score, minute, shooter, outcome, shot_position, shooter_info, shooter_stats, shooter_achievements, team_profile_away, team_profile_home):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, accurate single-sentence commentary describing an attempted shot.

STRICT RULES:
- Mention shooter, outcome, and position from which the shot was taken.
- No invented details.
- Mention exact event minute.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Shooter: SHOOTER
Outcome: OUTCOME
Position of the shot: SHOT_POSITION
SHOOTER Info: SHOOTER_INFO
SHOOTER Stats: SHOOTER_STATS
SHOOTER Achievements: SHOOTER_ACHIEVEMENTS

OUTPUT:
"Minute EVENT_MINUTE — SHOOTER fires a shot from SHOT_POSITION, but it’s OUTCOME. Score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Shooter: SHOOTER
Outcome: OUTCOME
Position of the shot: SHOT_POSITION
Shooter Info: SHOOTER_INFO
Shooter Stats: SHOOTER_STATS
Shooter Achievements: SHOOTER_ACHIEVEMENTS

OUTPUT:
"Minute EVENT_MINUTE — SHOOTER attempts a shot from SHOT_POSITION, but it goes OUTCOME. The score is still CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Shooter: {shooter}
Outcome: {outcome}
Position of the shot: {shot_position}
{shooter} Info: {shooter_info}
{shooter} Stats: {shooter_stats}
{shooter} Achievements: {shooter_achievements}

OUTPUT:"""

def prompt_dribbling(home_team, away_team, current_score, minute, dribbler, opponent, dribbler_info, dribbler_stats, success, team_profile_away, team_profile_home):
    return f"""TASK:
Describe in one energetic sentence a dribbling action between two players.

STRICT RULES:
- State clearly who dribbled who.
- Mention event minute.
- No invented details.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Dribbler: DRIBBLER
Defender: DEFENDER
Successful Dribbles: SUCCESSFUL_DRIBBLES

OUTPUT:
"Minute EVENT_MINUTE — DRIBBLER skilfully dribbles past DEFENDER, adding to his SUCCESSFUL_DRIBBLES successful dribbles this season. The score is CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Dribbler: DRIBBLER
Defender: DEFENDER

OUTPUT:
"At minute EVENT_MINUTE DRIBBLER elegantly dribbles past DEFENDER, keeping the pressure on at CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Dribbler: {dribbler}
Defender: {opponent}
{dribbler} Info: {dribbler_info}
{dribbler} Stats: {dribbler_stats}
Outcome: {success}

OUTPUT:"""


def prompt_tackle(home_team, away_team, current_score, minute, tackler, opponent, success, team_profile_away, team_profile_home):
    return f"""TASK:
Describe a football tackle in one sentence.

STRICT RULES:
- Mention tackler and opponent.
- Mention event minute.
- No invented context.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Tackler: TACKLER
Opponent: OPPONENT

OUTPUT:
"Minute EVENT_MINUTE — TACKLER executes a clean tackle against OPPONENT, halting the attack and keeping the score at CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Tackler: TACKLER
Opponent: OPPONENT

OUTPUT:
"At minute EVENT_MINUTE, TACKLER successfully challenges OPPONENT, disrupting their play and maintaining the current score of CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Tackler: {tackler}
Opponent: {opponent}
Success: {success}

OUTPUT:"""


def prompt_foul(home_team, away_team, current_score, minute, player, reason, card, player_info, player_stats, team_profile_away, team_profile_home):
    return f"""TASK:
Describe a foul event.

STRICT RULES:
- Mention fouling player, reason, and if given, the card color.
- Mention event minute.
- No invented details.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player: PLAYER
Reason: REASON
Card: CARD
Player Info: PLAYER_INFO
Player Stats: PLAYER_STATS  

OUTPUT:
"Minute EVENT_MINUTE — PLAYER commits a foul for REASON, receiving a CARD card. The score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player: PLAYER
Reason: REASON
Card: None
Player Info: PLAYER_INFO
Player Stats: PLAYER_STATS

OUTPUT:
"At minute EVENT_MINUTE, PLAYER is penalized for REASON but avoids a card. The score is still CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Player: {player}
Reason: {reason}
Card: {card}
{player} Info: {player_info}
{player} Stats: {player_stats}

OUTPUT:"""


def prompt_pass(home_team, away_team, current_score, minute, passer, receiver, pass_type, success, team_profile_away, team_profile_home):
    return f"""TASK:
Describe a pass in football.

STRICT RULES:
- Mention passer, receiver, pass type, and outcome.
- Mention event minute.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER
Pass Type: PASS_TYPE
Outcome: SUCCESS

OUTPUT:
"Minute EVENT_MINUTE — PASSER delivers a PASS_TYPE pass to RECEIVER, resulting in a successful play. The score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER
Pass Type: PASS_TYPE
Outcome: FAILURE

OUTPUT:
"At minute EVENT_MINUTE, PASSER attempts a PASS_TYPE pass to RECEIVER, but it fails to connect. The score stays at CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Passer: {passer}
Receiver: {receiver}
Pass Type: {pass_type}
Outcome: {success}

OUTPUT:"""


def prompt_var_call(home_team, away_team, current_score, minute, reason, team_profile_away, team_profile_home):
    return f"""TASK:
Describe a VAR review moment.

STRICT RULES:
- Mention reason for the review.
- Mention event minute.
- No invented details.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Reason: REASON

OUTPUT:
"At minute EVENT_MINUTE, the referee pauses the game for a VAR review due to REASON. The tension is palpable as everyone awaits the decision."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Reason: REASON

OUTPUT:
"Minute EVENT_MINUTE — VAR review underway following REASON. The match momentarily halts as officials review the play."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Reason: {reason}

OUTPUT:"""


def prompt_offside(home_team, away_team, current_score, minute, passer, receiver, team_profile_away, team_profile_home):
    return f"""TASK:
Describe an offside call.

STRICT RULES:
- Mention passer and receiver.
- Mention event minute.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER

OUTPUT:
"At minute EVENT_MINUTE, the assistant referee raises the flag for offside against RECEIVER after a pass from PASSER. The attack is stopped immediately."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER

OUTPUT:
"Minute EVENT_MINUTE — RECEIVER is caught offside following a through ball from PASSER, halting the promising move."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Passer: {passer}
Receiver: {receiver}

OUTPUT:"""


def prompt_start_end_game(home_team, away_team, minute, game_status, team_profile_away, team_profile_home):
    return f"""TASK:
Describe the start or end of the game in a single sentence.

STRICT RULES:
- Mention whether it’s the start or end.
- Mention the minute if relevant.
- No invented match events.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Event Minute: 0
Game Status: start

OUTPUT:
"The match between HOME_TEAM and AWAY_TEAM kicks off at minute 0, with both teams eager to make their mark."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Event Minute: 90
Game Status: end

OUTPUT:
"The final whistle blows at minute 90, bringing the exciting contest between HOME_TEAM and AWAY_TEAM to a close."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Event Minute: {minute}
Game Status: {game_status}

OUTPUT:"""


def prompt_substitution(home_team, away_team, current_score, minute, player_in, player_out, player_in_info, player_in_stats, player_out_info, player_out_stats, player_in_achievements, player_out_achievements,team_profile_away, team_profile_home):
    return f"""TASK:
Describe a substitution.

STRICT RULES:
- Mention player coming in and player going out.
- Mention event minute.
- Use provided player info and stats only.

EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: TEAM_PROFILE_HOME
Team Profile Away: TEAM_PROFILE_AWAY
Current Score: CURRENT_SCORE
Event Minute: 60
Player In: PLAYER_IN
Player Out: PLAYER_OUT
PLAYER_IN Info: AGE: 28, POSITION: MIDFIELDER
PLAYER_IN Stats: Appearances: 15, Goals: 3
PLAYER_OUT Info: AGE: 32, POSITION: MIDFIELDER
PLAYER_OUT Stats: Appearances: 20, Goals: 1
Player In Achievements: PLAYER_IN_ACHIEVEMENTS
Player Out Achievements: PLAYER_OUT_ACHIEVEMENTS

OUTPUT:
"Minute 60 — PLAYER_IN replaces PLAYER_OUT, bringing fresh energy to HOME_TEAM's midfield."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: TEAM_PROFILE_HOME
Team Profile Away: TEAM_PROFILE_AWAY
Current Score: CURRENT_SCORE
Event Minute: 75
Player In: PLAYER_IN
Player Out: PLAYER_OUT
Player In Info: AGE: 22, POSITION: FORWARD
Player In Stats: Appearances: 10, Goals: 7
Player Out Info: AGE: 30, POSITION: FORWARD
Player Out Stats: Appearances: 18, Goals: 5
Player In Achievements: PLAYER_IN_ACHIEVEMENTS
Player Out Achievements: PLAYER_OUT_ACHIEVEMENTS

OUTPUT:
"At minute 75, PLAYER_IN comes on for PLAYER_OUT to bolster HOME_TEAM's attacking options."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Player In: {player_in}
Player Out: {player_out}
{player_in} Info: {player_in_info}
{player_in} Stats: {player_in_stats}
{player_in} Achievements: {player_in_achievements}
{player_out} Info: {player_out_info}
{player_out} Stats: {player_out_stats}
{player_out} Achievements: {player_out_achievements}


OUTPUT:"""


def build_prompt(event_type, **kwargs):
    event_type = event_type.lower()

    events = {
        "goal": (prompt_goal, ["home_team", "away_team", "current_score", "minute", "scorer", "assist", "goal_type", "shot_position", "scorer_info", "scorer_stats", "scorer_achievements", "team_profile_away", "team_profile_home"]),
        "attempted_shot": (prompt_attempted_shot, ["home_team", "away_team", "current_score", "minute", "shooter", "outcome", "shot_position", "shooter_info", "shooter_stats", "shooter_achievements", "team_profile_away", "team_profile_home"]),
        "dribbling": (prompt_dribbling, ["home_team", "away_team", "current_score", "minute", "dribbler", "opponent", "dribbler_info", "dribbler_stats", "success", "team_profile_away", "team_profile_home"]),
        "tackle": (prompt_tackle, ["home_team", "away_team", "current_score", "minute", "tackler", "opponent", "success", "team_profile_away", "team_profile_home"]),
        "foul": (prompt_foul, ["home_team", "away_team", "current_score", "minute", "player", "reason", "card", "player_info", "player_stats",  "team_profile_away", "team_profile_home"]),
        "pass": (prompt_pass, ["home_team", "away_team", "current_score", "minute", "passer", "receiver", "pass_type", "success", "team_profile_away", "team_profile_home"]),
        "var_call": (prompt_var_call, ["home_team", "away_team", "current_score", "minute", "reason", "team_profile_away", "team_profile_home"]),
        "offside": (prompt_offside, ["home_team", "away_team", "current_score", "minute", "passer", "receiver", "team_profile_away", "team_profile_home"]),
        "start_end_game": (prompt_start_end_game, ["home_team", "away_team", "minute", "game_status", "team_profile_away", "team_profile_home"]),
        "substitution": (prompt_substitution, ["home_team", "away_team", "current_score", "minute", "player_in", "player_out", "player_in_info", "player_in_stats", "player_out_info", "player_out_stats", "player_in_achievements", "player_out_achievements", "team_profile_away", "team_profile_home"])
    }

    if event_type not in events:
        raise ValueError(f"❌ Unknown event type: {event_type}")

    func, required_params = events[event_type]

    missing = [p for p in required_params if p not in kwargs]
    if missing:
        raise ValueError(f"❌ Missing parameters for {event_type}: {missing}")

    # Richiama la funzione passando i parametri nell'ordine corretto
    return func(*[kwargs[p] for p in required_params])



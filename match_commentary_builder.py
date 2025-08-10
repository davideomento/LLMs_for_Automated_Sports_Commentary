def collect_match_context():
    print("=== Match Setup ===")
    home_team = input("Home team: ")
    away_team = input("Away team: ")
    game_week = input("Game week: ")

    print("\nEnter Premier League table (as JSON string or brief summary):")
    league_table = input("Table: ")

    print(f"\nEnter starting XI for {home_team} (comma-separated):")
    home_starting_xi = input().split(",")
    home_starting_xi = [player.strip() for player in home_starting_xi]

    home_coach = input(f"{home_team} Coach: ")

    print(f"\nEnter starting XI for {away_team} (comma-separated):")
    away_starting_xi = input().split(",")
    away_starting_xi = [player.strip() for player in away_starting_xi]

    away_coach = input(f"{away_team} Coach: ")

    return {
        "home_team": home_team,
        "away_team": away_team,
        "game_week": game_week,
        "league_table": league_table,
        "lineups": {
            home_team: {
                "starting_xi": home_starting_xi,
                "coach": home_coach
            },
            away_team: {
                "starting_xi": away_starting_xi,
                "coach": away_coach
            }
        }
    }
# Rememner to add attempted shots, blocked by, saved by, and other relevant stats to the context as needed.
def collect_match_event():
    print("\n=== Log New Match Event ===")
    minute = input("Minute of event: ")
    event_type = input("Event type (e.g., goal, assist, yellow_card): ").lower()

    event = {
        "minute": minute,
        "type": event_type
    }

    if event_type in {"goal", "assisted_goal", "penalty_scored", "shot_on_target", "shot_off_target", "blocked_shot", "yellow_card", "red_card", "foul_committed", "foul_won", "offside", "injury"}:
        event["player"] = input("Player involved: ")

    if event_type == "assisted_goal":
        event["assist_player"] = input("Assist by: ")

    if event_type == "own_goal":
        event["player"] = input("Player who scored own goal: ")
        event["opponent"] = input("Opponent team: ")

    if event_type == "substitution":
        event["player_off"] = input("Player off: ")
        event["player_on"] = input("Player on: ")
        event["team"] = input("Team making the substitution: ")

    if event_type == "penalty_missed":
        event["player"] = input("Penalty taker: ")

    if event_type == "penalty_saved":
        event["player"] = input("Penalty taker: ")
        event["keeper"] = input("Goalkeeper who saved: ")

    if event_type in {"corner", "free_kick", "penalty_awarded"}:
        event["team"] = input("Team awarded the set-piece: ")

    if event_type in {"kick_off", "half_time"}:
        event["team_kicking_off"] = input("Team kicking off: ")

    if event_type in {"full_time", "var_check", "var_decision"}:
        pass  

    return event


def main():
    match_context = collect_match_context()
    events = []

    while True:
        command = input("\nType 'add' to add a new event, 'view' to see events, or 'exit' to quit: ").lower()
        if command == "add":
            event = collect_match_event()
            events.append(event)
            print("✅ Event added.")
        elif command == "view":
            for idx, e in enumerate(events):
                print(f"{idx + 1}. {e}")
        elif command == "exit":
            break
        else:
            print("Unknown command.")

    print("\n=== Final Match Context and Events ===")
    print("Match Info:", match_context)
    print("Events:")
    for e in events:
        print(e)

if __name__ == "__main__":
    main()

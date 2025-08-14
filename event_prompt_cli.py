# ===== IMPORT YOUR TRANSFERMARKT FUNCTIONS =====
from transfermarkt_api import(
    search_player_by_name,
    get_player_info,
    get_player_stats, 
    get_player_achievements,
    get_competition_clubs,
    get_team_info,
    get_team_players,   
    search_competition_by_name
)
from prompt_builder import build_prompt 


def fetch_player_data(name):
    """Search player and fetch info, stats, achievements."""
    player_id = search_player_by_name(name)
    if not player_id:
        return None, None, None
    info = get_player_info(player_id)
    stats = get_player_stats(player_id)
    achievements = get_player_achievements(player_id)
    return info, stats, achievements



def main():
    print("=== Football Event Prompt Builder ===")
    
    competitions = {
        "1": "Premier League",
        "2": "La Liga",
        "3": "Serie A",
        "4": "Bundesliga",
        "5": "Ligue 1",
    }

    # Select competition
    print("\nSelect Competition:")
    for num, name in competitions.items():
        print(f"{num}. {name}")
    
    competition_choice = input("Enter choice number: ").strip()
    competition_name = competitions.get(competition_choice)
    if not competition_name:
        print("❌ Invalid competition choice.")
        return

    competition_id = search_competition_by_name(competition_name)
    if not competition_id:
        print(f"❌ Could not find ID for {competition_name}.")
        return

    comp_info = get_competition_clubs(competition_id)
    if not comp_info or "clubs" not in comp_info:
        print(f"❌ No clubs found for {competition_name}.")
        return

    clubs = comp_info["clubs"]

    # Display clubs
    print(f"\nSelect Home and Away Teams for {competition_name}:")
    for idx, club in enumerate(clubs, 1):
        print(f"{idx}. {club['name']}")

    try:
        home_idx = int(input("Select Home Team number: ").strip())
        away_idx = int(input("Select Away Team number: ").strip())
        home_team = clubs[home_idx - 1]
        away_team = clubs[away_idx - 1]
    except (ValueError, IndexError):
        print("❌ Invalid team selection.")
        return

    home_info = get_team_info(home_team['id'])
    home_stats = get_team_players(home_team['id'])
    away_info = get_team_info(away_team['id'])
    away_stats = get_team_players(away_team['id'])

    minute = input("Enter event minute: ").strip()

    event_types = {
        "1": "goal",
        "2": "foul",
        "3": "attempted_shot",
        "4": "dribbling",
        "5": "tackle",
        "6": "pass",
        "7": "var_call",
        "8": "offside",
        "9": "start_end_game",
        "10": "substitution"
    }

    print("\nSelect Event Type:")
    for num, name in event_types.items():
        print(f"{num}. {name.capitalize()}")
    
    choice = input("Enter choice number: ").strip()
    event_type = event_types.get(choice)
    if not event_type:
        print("❌ Invalid choice.")
        return

    kwargs = {
        "minute": minute,
        "competition": competition_name,
        "home_team": home_team['name'],
        "away_team": away_team['name'],
        "home_team_info": home_info,
        "home_team_stats": home_stats,
        "away_team_info": away_info,
        "away_team_stats": away_stats,
        "current_score": input("Current score (e.g., 1-0): ")
    }

    # ==== Team and player selection for applicable events ====
    if event_type not in ["var_call", "start_end_game"]:
        print("\nSelect the team involved in the event:")
        print(f"1. {home_team['name']}")
        print(f"2. {away_team['name']}")
        team_choice = input("Enter team number: ").strip()

        if team_choice == "1":
            selected_team_name = home_team['name']
            selected_team_players = home_stats
        elif team_choice == "2":
            selected_team_name = away_team['name']
            selected_team_players = away_stats
        else:
            print("❌ Invalid team choice.")
            return

        print(f"\nSelect player from {selected_team_name}:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        player_idx = input("Enter player number: ").strip()
        try:
            player_idx = int(player_idx) - 1
            player_name = selected_team_players[player_idx]['name']
        except (ValueError, IndexError):
            print("❌ Invalid player selection.")
            return

        player_info, player_stats, player_achievements = fetch_player_data(player_name)
        if not player_info:
            print(f"❌ Could not fetch data for player {player_name}")
            return

    # ==== Map input parameters to prompt-required names ====
    if event_type == "goal":
        goal_types = {"1": "Right foot", "2": "Left foot", "3": "Header", "4": "Other"}
        shot_positions = {"1": "Inside box", "2": "Outside box", "3": "Penalty spot"}
        print("\nGoal type options:")
        for k, v in goal_types.items(): print(f"{k}. {v}")
        goal_type = goal_types.get(input("Select goal type: "), "Unknown")

        print("\nShot position options:")
        for k, v in shot_positions.items(): print(f"{k}. {v}")
        shot_position = shot_positions.get(input("Select shot position: "), "Unknown")

        assist = input("Assist name (or leave blank): ")

        # Map to prompt parameters
        kwargs.update({
            "scorer": player_name,
            "scorer_info": player_info,
            "scorer_stats": player_stats,
            "scorer_achievements": player_achievements,
            "assist": assist,
            "goal_type": goal_type,
            "shot_position": shot_position
        })

    elif event_type == "attempted_shot":
        shot_outcomes = {"1": "Saved", "2": "Missed", "3": "Blocked"}
        shot_positions = {"1": "Inside box", "2": "Outside box", "3": "Penalty spot"}
        print("\nShot outcome options:")
        for k, v in shot_outcomes.items(): print(f"{k}. {v}")
        outcome = shot_outcomes.get(input("Select outcome number: "), "Unknown")

        print("\nShot position options:")
        for k, v in shot_positions.items(): print(f"{k}. {v}")
        shot_position = shot_positions.get(input("Select position number: "), "Unknown")

        kwargs.update({
            "shooter": player_name,
            "shooter_info": player_info,
            "shooter_stats": player_stats,
            "shooter_achievements": player_achievements,
            "outcome": outcome,
            "shot_position": shot_position
        })

    elif event_type == "dribbling":
        print("Select defender from opposing team:")
        opposing_team_players = home_stats if selected_team_name == away_team['name'] else away_stats
        for idx, player in enumerate(opposing_team_players, 1):
            print(f"{idx}. {player['name']}")
        defender_idx = input("Enter defender number: ").strip()
        try:
            defender_idx = int(defender_idx) - 1
            defender_name = opposing_team_players[defender_idx]['name']
        except (ValueError, IndexError):
            print("❌ Invalid defender selection.")
            return

        kwargs.update({
            "player1": player_name,
            "player1_info": player_info,
            "player1_stats": player_stats,
            "player2": defender_name
        })

    elif event_type == "tackle":
        print("Select opponent from opposing team:")
        opposing_team_players = home_stats if selected_team_name == away_team['name'] else away_stats
        for idx, player in enumerate(opposing_team_players, 1):
            print(f"{idx}. {player['name']}")
        opponent_idx = input("Enter opponent number: ").strip()
        try:
            opponent_idx = int(opponent_idx) - 1
            opponent_name = opposing_team_players[opponent_idx]['name']
        except (ValueError, IndexError):
            print("❌ Invalid opponent selection.")
            return

        kwargs.update({
            "tackler": player_name,
            "opponent": opponent_name
        })

    elif event_type == "foul":
        foul_reasons = {"1": "Handball", "2": "Tripping", "3": "Pushing", "4": "Other"}
        card_types = {"1": "Yellow", "2": "Red", "3": "None"}
        print("\nFoul reason options:")
        for k, v in foul_reasons.items(): print(f"{k}. {v}")
        reason = foul_reasons.get(input("Select reason number: "), "Unknown")
        print("\nCard options:")
        for k, v in card_types.items(): print(f"{k}. {v}")
        card = card_types.get(input("Select card number: "), "None")

        kwargs.update({
            "player": player_name,
            "reason": reason,
            "card": card,
            "player_info": player_info,
            "player_stats": player_stats,
        })

    elif event_type == "pass":
        pass_types = {"1": "Short", "2": "Long", "3": "Through"}
        outcomes = {"1": "Success", "2": "Fail"}
        print("\nPass type options:")
        for k, v in pass_types.items(): print(f"{k}. {v}")
        pass_type = pass_types.get(input("Select pass type number: "), "Unknown")

        print("\nPass outcome options:")
        for k, v in outcomes.items(): print(f"{k}. {v}")
        success = outcomes.get(input("Select outcome number: "), "Unknown")

        print("Select receiver from same team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        receiver_idx = int(input("Enter receiver number: ").strip()) - 1
        receiver_name = selected_team_players[receiver_idx]['name']

        kwargs.update({
            "passer": player_name,
            "receiver": receiver_name,
            "pass_type": pass_type,
            "success": success
        })

    elif event_type == "offside":
        print("Select receiver from same team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        receiver_idx = int(input("Enter receiver number: ").strip()) - 1
        receiver_name = selected_team_players[receiver_idx]['name']

        kwargs.update({
            "passer": player_name,
            "receiver": receiver_name
        })

    elif event_type == "var_call":
        kwargs.update({
            "reason": input("Reason for VAR review: ")
        })

    elif event_type == "start_end_game":
        kwargs.update({
            "game_status": input("Game status (start/end): ")
        })

    elif event_type == "substitution":
        print("Select player coming in:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        in_idx = int(input("Enter player in number: ").strip()) - 1
        player_in = selected_team_players[in_idx]['name']
        in_info, in_stats, in_achievements = fetch_player_data(player_in)

        print("Select player going out:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        out_idx = int(input("Enter player out number: ").strip()) - 1
        player_out = selected_team_players[out_idx]['name']
        out_info, out_stats, out_achievements = fetch_player_data(player_out)

        kwargs.update({
            "player_in": player_in,
            "player_in_info": in_info,
            "player_in_stats": in_stats,
            "player_in_achievements": in_achievements,
            "player_out": player_out,
            "player_out_info": out_info,
            "player_out_stats": out_stats,
            "player_out_achievements": out_achievements
        })

    print("\n✅ Event data collected successfully!")

    try:
        # Build the final prompt
        prompt = build_prompt(event_type, **kwargs)
        print("\n=== Generated Prompt ===")
        print(prompt)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()












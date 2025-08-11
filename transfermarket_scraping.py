import requests

BASE_URL = "http://127.0.0.1:8000"

def search_team_by_name(name):
    url = f"{BASE_URL}/clubs/search/{name}"
    response = requests.get(url)
    if response.ok:
        results = response.json()
        if results and 'results' in results and len(results['results']) > 0:
            return results['results'][0]['id']
        else:
            print(f"No team found with the name '{name}'")
            return None
    else:
        print(f"Error searching team: {response.status_code}")
        return None


def search_player_by_name(name):
    url = f"{BASE_URL}/players/search/{name}"
    response = requests.get(url)
    if response.ok:
        results = response.json()
        if results and 'results' in results and len(results['results']) > 0:
            return results['results'][0]['id']
        else:
            print(f"No player found with the name '{name}'")
            return None
    else:
        print(f"Error searching player: {response.status_code}")
        return None

def get_team_info(club_id):
    url = f"{BASE_URL}/clubs/{club_id}/profile"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving team info for {club_id}: {response.status_code}")
        return None
    
def get_team_players(club_id):
    url = f"{BASE_URL}/clubs/{club_id}/players"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving players for {club_id}: {response.status_code}")
        return None
    
def get_player_info(player_id):
    url = f"{BASE_URL}/players/{player_id}/profile"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player info for {player_id}: {response.status_code}")
        return None

def get_player_stats(player_id):
    url = f"{BASE_URL}/players/{player_id}/stats"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player stats for {player_id}: {response.status_code}")
        return None

def get_player_achievements(player_id):
    url = f"{BASE_URL}/players/{player_id}/achievements"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player achievements for {player_id}: {response.status_code}")
        return None

if __name__ == "__main__":
    team_a_name = input("Enter Team A name: ")
    team_b_name = input("Enter Team B name: ")
    player_name = input("Enter player name: ")

    team_a_id = search_team_by_name(team_a_name)
    team_b_id = search_team_by_name(team_b_name)
    player_id = search_player_by_name(player_name)

    if team_a_id:
        print("\nTEAM A INFO:")
        team_a_info = get_team_info(team_a_id)
        team_a_players = get_team_players(team_a_id)
        print(team_a_info)
        print("\nTeam A Players:")
        print(team_a_players)

    if team_b_id:
        print("\nTEAM B INFO:")
        team_b_info = get_team_info(team_b_id)
        team_b_players = get_team_players(team_b_id)
        print(team_b_info)
        print("\nTeam B Players:")
        print(team_b_players)


    if player_id:
        print("\nPLAYER INFO:")
        player_info = get_player_info(player_id)
        print(player_info)

        print("\nPLAYER STATS:")
        player_stats = get_player_stats(player_id)
        print(player_stats)

        print("\nPLAYER ACHIEVEMENTS:")
        player_achievements = get_player_achievements(player_id)
        print(player_achievements)

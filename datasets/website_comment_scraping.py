import requests
import json
import os
from datetime import datetime, timedelta

start_date = datetime.strptime("2024-10-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-10-30", "%Y-%m-%d")




# Tua API key e host
headers = {
    'x-rapidapi-key': '2ba638dd6eb04ac5cf6031eb486566cc',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

# Massimi campionati europei (id tipici o nomi; devi verificare con la tua API)
top_leagues = {
    39: "Premier League",
    135: "Serie A",
    140: "La Liga",
    78: "Bundesliga",
    61: "Ligue 1"
}

# Data e url base
url_fixtures = "https://v3.football.api-sports.io/fixtures"
url_events = "https://v3.football.api-sports.io/fixtures/events"

all_matches = []

current_date = start_date
matches_with_comments = []

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    querystring_fixtures = {"date": date_str}
    response = requests.get(url_fixtures, headers=headers, params=querystring_fixtures)
    data = response.json()


    for fixture in data['response']:
        league_id = fixture['league']['id']
        # Filtro solo massimi campionati
        if league_id not in top_leagues:
            continue

        fixture_id = fixture['fixture']['id']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']

        # Prendo eventi/commenti partita
        querystring_events = {"fixture": fixture_id}
        response_events = requests.get(url_events, headers=headers, params=querystring_events)
        events_data = response_events.json()

        if 'response' not in events_data or len(events_data['response']) == 0:
            # Nessun evento disponibile, salto partita
            continue

        # Creo lista minuti e commenti (se commenti esistono)
        minute_comment_pairs = []
        for event in events_data['response']:
            minute = event.get('time', {}).get('elapsed')
            comment = event.get('detail')  # o event.get('comments') se presente nella struttura
            # Considera solo se commento disponibile e minuto
            if minute is not None and comment:
                minute_comment_pairs.append({
                    "minute": minute,
                    "comment": comment
                })

        if len(minute_comment_pairs) == 0:
            # Nessun commento utile, salto
            continue

        matches_with_comments.append({
            "fixture_id": fixture_id,
            "home_team": home_team,
            "away_team": away_team,
            "comments": minute_comment_pairs
        })

    current_date += timedelta(days=1)



# Salvo il risultato in JSON
os.makedirs("data/api_football", exist_ok=True)

with open("data/api_football/matches_comments.json", "w", encoding="utf-8") as f:
    json.dump(matches_with_comments, f, ensure_ascii=False, indent=4)

print(f"File generato con {len(matches_with_comments)} partite con commenti.")

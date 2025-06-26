import http.client
import json

API_HOST = "v3.football.api-sports.io"
API_KEY  = "2ba638dd6eb04ac5cf6031eb486566cc"
HEADERS = {
    'x-rapidapi-host': API_HOST,
    'x-rapidapi-key': API_KEY
}

conn = http.client.HTTPSConnection(API_HOST)

# 1) Prendo l'ultima partita disponibile (qualsiasi stato) di Serie A 2023
league_id = 135   # Serie A
season    = 2023  # 2023–24
params = f"league={league_id}&season={season}&sort=date&order=desc&limit=1"
conn.request("GET", f"/fixtures?{params}", headers=HEADERS)
res = conn.getresponse()
fixtures_resp = json.loads(res.read().decode("utf-8"))

fixtures = fixtures_resp.get("response", [])
if not fixtures:
    raise SystemExit("❌ Nessun fixture trovato per Serie A 2023 (senza status).")

# Estrai i dati base della prima partita
first = fixtures[0]
fixture_id = first["fixture"]["id"]
home = first["teams"]["home"]["name"]
away = first["teams"]["away"]["name"]
date = first["fixture"]["date"][:10]

print(f"🏟️ Partita selezionata: {home} vs {away} (ID {fixture_id}, data {date})\n")

# 2) Recupero i dettagli completi dello stesso fixture
conn.request("GET", f"/fixtures?id={fixture_id}", headers=HEADERS)
res2 = conn.getresponse()
details = json.loads(res2.read().decode("utf-8"))

# 3) Stampo il JSON formattato in terminale
print(json.dumps(details, indent=4, ensure_ascii=False))

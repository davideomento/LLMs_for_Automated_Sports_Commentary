import requests
from bs4 import BeautifulSoup
import urllib.parse

BASE_API_URL = "https://transfermarkt-api.fly.dev"

def find_player_id(full_name):
    """Cerca l'ID del giocatore su Transfermarkt tramite scraping."""
    base_search_url = "https://www.transfermarkt.it/schnellsuche/ergebnis/schnellsuche?query="
    query = urllib.parse.quote(full_name)
    url = base_search_url + query

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    players_table = soup.find('table', class_='items')

    if not players_table:
        raise ValueError(f"Nessun risultato giocatore trovato per '{full_name}'.")

    first_row = players_table.find('tbody').find('tr')
    player_link = first_row.find('a', href=True)
    href = player_link['href']  # es. /kylian-mbappe/profil/spieler/342229

    parts = href.split('/')
    player_id = None
    for i, part in enumerate(parts):
        if part == 'spieler':
            player_id = int(parts[i + 1])
            break

    if player_id is None:
        raise ValueError("Impossibile estrarre l'ID giocatore.")

    return player_id

def get_player_data(player_id):
    """Recupera i dati del giocatore dall'API transfermarkt-api."""
    url = f"{BASE_API_URL}/players/{player_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    nome_completo = "Kylian Mbappé"  # Cambia qui con nome e cognome del giocatore
    try:
        print(f"Sto cercando l'ID di {nome_completo}...")
        player_id = find_player_id(nome_completo)
        print(f"ID trovato: {player_id}")

        print(f"Ottenendo i dati di {nome_completo} dall'API...")
        dati = get_player_data(player_id)

        print("\n--- Dati giocatore ---")
        for k, v in dati.items():
            print(f"{k}: {v}")

    except Exception as e:
        print(f"Errore: {e}")

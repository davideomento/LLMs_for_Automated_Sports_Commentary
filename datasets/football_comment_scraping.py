import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Step 1 – Estrai gli URL delle partite da una data
def get_match_urls_from_scores_fixtures(date_str):
    base_url = f"https://www.bbc.com/sport/football/scores-fixtures/{date_str}"
    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        print(f"⚠️ Failed to fetch match list for {date_str}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    match_urls = set()
    for link in links:
        href = link["href"]
        if "/sport/live/football/" in href:
            full_url = "https://www.bbc.com" + href.split("?")[0]  # Clean query params
            match_urls.add(full_url)

    return list(match_urls)

# Step 2 – Estrai la cronaca testuale da un singolo URL
def scrape_bbc_commentary(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to retrieve: {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = soup.find_all("div", class_="lx-commentary__event")

    commentary_data = []
    for event in events:
        minute_tag = event.find("span", class_="lx-commentary__time")
        text_tag = event.find("p", class_="lx-commentary__body")

        if minute_tag and text_tag:
            commentary_data.append({
                "minute": minute_tag.get_text(strip=True),
                "text": text_tag.get_text(strip=True)
            })

    return commentary_data

# Step 3 – Loop su più giorni e salva le cronache
def collect_commentaries(start_date, end_date, output_file="bbc_all_commentaries.json"):
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"\n📅 Processing matches on {date_str}")
        match_urls = get_match_urls_from_scores_fixtures(date_str)

        for url in match_urls:
            print(f"🔍 Scraping: {url}")
            commentary = scrape_bbc_commentary(url)
            if commentary:
                all_data.append({
                    "date": date_str,
                    "url": url,
                    "commentary": commentary
                })
            time.sleep(1.5)  # Rispetta i limiti del server

        current_date += timedelta(days=1)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Finished scraping. Total matches saved: {len(all_data)}")

# === MAIN ===
if __name__ == "__main__":
    # Imposta l'intervallo di date (esempio: 1 settimana)
    start = datetime.strptime("2024-06-01", "%Y-%m-%d")
    end = datetime.strptime("2024-06-07", "%Y-%m-%d")

    collect_commentaries(start, end)

# LLMs_for_Automated_Sports_Commentary
My Master's Thesis in Mathematical Engineering

## Procedure
- Find dataset to RAG
- Use ElasticSearch to RAG new events that are not in the dataset
- Find golden-standard dataset with accurate and rich comment

### Website, RAG dataset
For now I used FantasyPremierLeague, I only considered last 3 seasons and  generated textual description for each seasons and for each games week for each player.

1)	https://www.football-data.co.uk/
•  CSV con risultati, date, squadre, goal, xG, etc. (Serie A inclusa).
•  Perfetto per basi statistiche.
2)	https://github.com/statsbomb/open-data
•  Estremamente dettagliato (eventi in campo, passaggi, tiri).
•  Include alcuni campionati (non Serie A), ma puoi usarlo per prototipi.
3)	https://www.transfermarkt.com/
•  Profili giocatori, statistiche stagionali, cronologia gol, assist, etc.
•  Puoi costruirti un dataset RAG-friendly.
4)	https://www.kaggle.com/datasets/hugomathien/soccer
•  Database SQLite con partite, squadre, player data (2008–2016).
5)	https://www.whoscored.com/
•  Molto dettagliato ma da usare con cautela per TOS.


### Dataset BBC webscraping and Event kaggle
Limitations: Just a brief description of the event, not a real comment

### Dataset from youtube commentaries
Pro: Very rich comment, with insights, statistics ecc
Cons: Difficult allineate events and comment, but I could use gpt4 to do that for me

### Dataset from website trough API
Contacted them, waiting for a response:
- https://www.api-football.com/
- https://sportradar.com/
- https://www.statsperform.com/
- https://www.football-data.org/
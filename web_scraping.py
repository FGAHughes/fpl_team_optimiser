import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time

# list of league urls that contain all players from that league last season. Only leagues where strong players will translate to pl
league_urls = ['https://fbref.com/en/comps/9/stats/Premier-League-Stats',
        'https://fbref.com/en/comps/12/stats/La-Liga-Stats',
        'https://fbref.com/en/comps/20/stats/Bundesliga-Stats',
        'https://fbref.com/en/comps/13/stats/Ligue-1-Stats',
        'https://fbref.com/en/comps/11/stats/Serie-A-Stats',
        'https://fbref.com/en/comps/32/stats/Primeira-Liga-Stats',
        'https://fbref.com/en/comps/23/stats/Eredivisie-Stats',
        'https://fbref.com/en/comps/10/stats/Championship-Stats'
        ]

# List of every Premier League player in the 2025/26 season
pl_players = 'https://fbref.com/en/comps/9/2025-2026/wages/2025-2026-Premier-League-Wages'

def scrape_league_dfs(urls):

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if 'id="stats_standard"' in comment:
                table_soup = BeautifulSoup(comment, 'html.parser')
                break
        table = table_soup.find('table', {'id': 'stats_standard'})
        df = pd.read_html(str(table), skiprows=1)[0]
        df.drop(['Rk', 'Matches'],inplace=True, axis=1)
        df.to_csv(f'csvs/league_csvs/{url.split("/")[-1]}.csv', index=False)
        print(df.head())
        time.sleep(5)


scrape_league_dfs(urls=league_urls)
# print(league_urls[0].split("/")[-1])
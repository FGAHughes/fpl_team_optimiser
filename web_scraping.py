import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# list of league urls that contain all players from that league last season. Only leagues where strong players will translate to pl
league_urls = ['https://fbref.com/en/comps/9/stats/Premier-League-Stats',
               'https://fbref.com/en/comps/12/stats/La-Liga-Stats',
               'https://fbref.com/en/comps/20/stats/Bundesliga-Stats',
               'https://fbref.com/en/comps/13/stats/Ligue-1-Stats',
               'https://fbref.com/en/comps/11/stats/Serie-A-Stats',
               'https://fbref.com/en/comps/32/stats/Primeira-Liga-Stats',
               'https://fbref.com/en/comps/23/stats/Eredivisie-Stats',
               'https://fbref.com/en/comps/10/stats/Championship-Stats',
               'https://fbref.com/en/comps/9/2020-2021/stats/2020-2021-Premier-League-Stats'
               ]
pl_urls = ['https://fbref.com/en/comps/9/stats/Premier-League-Stats',
           'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats',
           'https://fbref.com/en/comps/9/2022-2023/stats/2022-2023-Premier-League-Stats',
           'https://fbref.com/en/comps/9/2021-2022/stats/2021-2022-Premier-League-Stats',
           'https://fbref.com/en/comps/9/2019-2020/stats/2019-2020-Premier-League-Stats',
           'https://fbref.com/en/comps/9/2018-2019/stats/2018-2019-Premier-League-Stats',
           'https://fbref.com/en/comps/9/2017-2018/stats/2017-2018-Premier-League-Stats'
           ]
fpl_season_urls = ['https://www.premierfantasytools.com/2023-24-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2022-23-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2021-22-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2020-21-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2019-20-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2018-19-fpl-end-of-season-player-data/',
                   'https://www.premierfantasytools.com/2017-18-fpl-end-of-season-player-data/'
                   ]

# List of every Premier League player in the 2025/26 season
pl_players_url = 'https://fbref.com/en/comps/9/2025-2026/wages/2025-2026-Premier-League-Wages'

# fpl_season_urls = ['https://www.premierfantasytools.com/2018-19-fpl-end-of-season-player-data/']


def scrape_league_dfs(urls, path):
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
        df.drop(['Rk', 'Nation', 'Squad', 'Matches'], inplace=True, axis=1)
        df.to_csv(f'{path}{url.split("/")[-1]}.csv', index=False)
        time.sleep(3)


def scrape_pl_players(url):
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = [col[1] if isinstance(col, tuple) else col for col in df.columns]
    df = df.dropna(how='all')
    df = df[['Player', 'Squad']]
    df.to_csv(f'csvs/player_csvs/2526_players.csv', index=False)


def scrape_df_with_pandas(urls):
    for i in range(len(urls)):
        url = urls[i]
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        tables = pd.read_html(resp.text)
        df = tables[1]
        if i != 4:
            df.columns = df.iloc[0]
            df = df.drop(index=0, axis=0).reset_index(drop=True)
        df.columns = [j for j in range(len(df.columns))]
        df = df[[0, len(df.columns)-1]]
        df.columns = ['full_name', 'total_points']
        season = (url.split('/')[-2]).split('-fpl-end-of-season-player-data')[0]
        df.to_csv(f'csvs/fpl_csvs/{season}_total_points.csv')
        print(df.head())
        time.sleep(3)



def fetch_2425_pl_data():
    main_response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    df = pd.json_normalize(main_response.json(), record_path='elements')
    df = df[['web_name',
             'first_name',
             'second_name',
             'total_points'
             ]]
    df['full_name'] = df['first_name'] + ' ' + df['second_name']
    df.drop(['web_name', 'first_name', 'second_name'], axis=1, inplace=True)
    df = df[['full_name', 'total_points']]
    df.to_csv('csvs/fpl_csvs/2024-25_total_points.csv')


scrape_df_with_pandas(urls=fpl_season_urls)
fetch_2425_pl_data()
scrape_league_dfs(urls=league_urls, path='csvs/league_csvs/')
scrape_league_dfs(urls=pl_urls, path='csvs/pl_csvs/')
scrape_pl_players(url=pl_players_url)

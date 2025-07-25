import pandas as pd
import os
import time


pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def remove_subheaders(path):
    df = pd.read_csv(path)
    player_index = df[(df.Player == 'Player')].index
    df.drop(index=player_index, axis=0, inplace=True)
    return df

# bring in all stats from the previous season for all premier league players, excluding those from weak leagues and limited if the player's name has changed in fbref (which is rare)
def create_2526_player_list():
    player_list = remove_subheaders('csvs/player_csvs/2526_players.csv')

    csvs = os.listdir('csvs/league_csvs/')
    # Move pl to start as it will have the most matches on merge
    csvs.remove('Premier-League-Stats.csv')
    csvs.insert(0, 'Premier-League-Stats.csv')

    pl_add = player_list.copy()
    for i in range(len(csvs)):
        if i == 0:
            df = remove_subheaders(f'csvs/league_csvs/{csvs[i]}')
            pl_add = pl_add.merge(how='left', on='Player', right=df)
            pl_remaining = pl_add[pl_add.Pos.isna()].copy()
            pl_add.dropna(inplace=True, axis=0)
            league = csvs[i].split("-Stats.csv", 1)[0]
            pl_add['league'] = league
            pl_master = pl_add

        else:
            df = remove_subheaders(f'csvs/league_csvs/{csvs[i]}')
            pl_remaining = pd.DataFrame(data=pl_remaining[['Player', 'Squad']])
            pl_add = pl_remaining.merge(how='left', on='Player', right=df)
            pl_remaining = pl_add[pl_add.Pos.isna()].copy()
            pl_add.dropna(inplace=True, axis=0)
            league = csvs[i].split("-Stats.csv", 1)[0]
            pl_add['league'] = league
            pl_master = pd.concat(objs=[pl_master, pl_add], axis=0)

    pl_master.to_csv('csvs/player_csvs/2526_players_with_stats.csv', index=False)

create_2526_player_list()
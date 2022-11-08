import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from src.Utils.Dictionaries import team_index_07, team_index_08, team_index_12, team_index_13, team_index_14, team_index_current

season_array = [
                # "2007-08", 
                # "2008-09", 
                # "2009-10", 
                # "2010-11", 
                # "2011-12", 
                # "2012-13", 
                # "2013-14",
                # "2014-15",
                # "2015-16",
                # "2016-17", 
                # "2017-18", 
                # "2018-19", 
                # "2019-20", # -> 데이터 오류로 미사용
                # "2020-21", 
                # "2021-22"
                "2022-23"
                ]
odds_directory = os.fsdecode('Odds-Data/Odds-Data-Clean')
df = pd.DataFrame
scores = []
win_margin = []
OU = []
OU_Cover = []
games = []

def create_game():
    for season in tqdm(season_array):
        file = pd.read_excel(odds_directory + '/' + '{}.xlsx'.format(season))
        print(file)

        team_data_directory = os.fsdecode('TeamData/{}'.format(season))
        for row in file.itertuples():
            # print(row)
            home_team = row[3]
            away_team = row[4]
            date = row[2]
            date_array = date.split('-')
            year = date_array[0] + '-' + date_array[1]
            month = date_array[2][:2]
            day = date_array[2][2:]

            if month[0] == '0':
                month = month[1:]
            if day[0] == '0':
                day = day[1:]

            team_data_file = month + '-' + day + '-' + year + '.xlsx'
            
            data_frame = pd.read_excel(team_data_directory + '/' + team_data_file)
            print(data_frame)
            if len(data_frame.index) == 30:
                score = float(row[9])
                ou = row[5]
                margin = float(row[10])
                
                if str(ou).find("o") != -1:
                    ou = float(str(ou).split("o")[0])
                elif str(ou).find("u") != -1:
                    ou = float(str(ou).split("u")[0])
                
                scores.append(score)
                OU.append(ou)
                
                if margin > 0:
                    win_margin.append(1)
                else:
                    win_margin.append(0)

                if score < ou:
                    OU_Cover.append(0)
                elif score > ou:
                    OU_Cover.append(1)
                elif score == ou:
                    OU_Cover.append(2)
                
                print(home_team, away_team)
                if season == '2007-08':
                    home_team_series = data_frame.iloc[team_index_07.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_07.get(away_team)]
                elif season == '2008-09' or season == "2009-10" or season == "2010-11" or season == "2011-12":
                    home_team_series = data_frame.iloc[team_index_08.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_08.get(away_team)]
                elif season == "2012-13":
                    home_team_series = data_frame.iloc[team_index_12.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_12.get(away_team)]
                elif season == '2013-14':
                    home_team_series = data_frame.iloc[team_index_13.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_13.get(away_team)]                
                elif season == '2014-15':
                    home_team_series = data_frame.iloc[team_index_14.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_14.get(away_team)]
                else:
                    home_team_series = data_frame.iloc[team_index_current.get(home_team)]
                    away_team_series = data_frame.iloc[team_index_current.get(away_team)]

                game = pd.concat([home_team_series, away_team_series])
                games.append(game)
            
        frame = pd.concat(games, ignore_index=True, axis=1)
        frame = frame.T
        frame = frame.drop(columns=['TEAM_ID', 'CFID', 'CFPARAMS', 'Unnamed: 0'])
        frame['Score'] = np.asarray(scores)
        frame['Home-Team-Win'] = np.asarray(win_margin)
        frame['OU'] = np.asarray(OU)
        frame['OU-Cover'] = np.asarray(OU_Cover)
        frame.to_excel(f'Datasets/Full-Data-Set-UnderOver-{season}.xlsx')
        print(f"{season} DONE!")
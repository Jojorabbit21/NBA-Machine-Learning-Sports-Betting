import os
import pandas as pd
from tqdm import tqdm
from src.Utils.Dictionaries import team_codes, team_codes_after_1314

directory = os.fsdecode('Odds-Data')

def create_odds_data(season_from:str, season_to:str=None):
    seasons = []
    
    for i in range(int(season_from), int(season_to)):
        seasons.append(i)
        
    for season in seasons:
        season_suffix = int(str(season)[-2:]) + 1
        file = "nba odds " + str(season) + "-" + str(season_suffix) + ".xlsx"
        if file not in os.listdir(directory):
            print(f"NO FILE OF {file}")
            pass
        print(file)
        df = pd.read_excel(directory + "/" + file)
        x = pd.DataFrame(columns=['Date', 'Home', 'Away', 'OU', 'Spread', 'ML_Home', 'ML_Away', 'Points', 'Win_Margin'])
        count = 2
        date = ''
        home = ''
        away = ''
        ou = ''
        spread = ''
        ml_home = ''
        ml_away = ''
        points = ''
        margin = ''
        year = str(season) + "-" + str(season_suffix)
        for row in tqdm(df.itertuples()):
            if count % 2 == 0:
                if len(str(row[1])) == 3:
                    date = str(year + '-' + '0' + str(row[1]))
                else:
                    date = str(year + '-' + str(row[1]))
                away = team_codes.get(str(row[4]))
                if row[10] == 'pk':
                    ou = 0
                else:
                    ou = row[10]
                points = row[9]
                ml_away = str(row[12])
                count += 1
            else:
                home = team_codes.get(str(row[4]))
                if row[10] == 'pk':
                    spread = 0
                else:
                    spread = row[10]
                if spread > 50:
                    temp = spread
                    spread = ou
                    ou = temp
                ml_home = str(row[12])
                margin = row[9] - points
                points += row[9]
                temp = {
                    'Date': date,
                    'Home': home,
                    'Away': away,
                    'OU': ou,
                    'Spread': spread,
                    'ML_Home': ml_home,
                    'ML_Away': ml_away,
                    'Points': points,
                    'Win_Margin': margin
                }
                temp = pd.DataFrame.from_dict([temp])
                x = pd.concat([x, temp], ignore_index=True)
                count += 1
                date = ''
                home = ''
                away = ''
                ou = ''
                spread = ''
                ml_home = ''
                ml_away = ''
                points = ''
                margin = ''
        directory2 = os.fsdecode('Odds-Data/Odds-Data-Clean')
        name = directory2 + '/' + year + '.xlsx'
        print(name)
        x.to_excel(name)

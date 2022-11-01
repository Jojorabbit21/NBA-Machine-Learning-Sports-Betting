import pandas as pd
import requests
import datetime
import json

from src.Utils.Dictionaries import full_to_abbr
from src.Utils.tools import decimal_to_american

API_KEY = '41c7393c20msh234decbf759c97cp128eecjsn982ef9811694'
API_HOST = 'api-basketball.p.rapidapi.com'
API_URL = {
  'games': 'https://api-basketball.p.rapidapi.com/games',
  'odds': 'https://api-basketball.p.rapidapi.com/odds'
}
API_LEAGUE = 12
API_TZ = 'Asia/Seoul'
API_SEASON = '2022-2023'
API_BOOKMAKER = 12 # Pinnacle
BETTYPE = [
  2, # 2way
  4  # Ou
]

class Odds():
  def request_data(self, date):
    if date is None:
      date = datetime.datetime.today().strftime("%Y-%m-%d")
    querystring = {
      "timezone": API_TZ,
      "season": API_SEASON,
      "league": API_LEAGUE,
      "date": date
    }
    headers = {
      "X-RapidAPI-Key": API_KEY,
      "X-RapidAPI-Host": API_HOST,
    }
    response = requests.get(API_URL['games'], headers=headers, params=querystring)
    data = response.json()['response']
    gameids = []
    for key in data:
      gameids.append(key['id'])
    return gameids
  
  def build_data(self, ids):
    hteam = []; ateam = []; hodds = []; aodds = []; total = []
    date = datetime.datetime.now().strftime('%Y%m%d')
    for id in ids:
      querystring = { 
                      "league": API_LEAGUE,
                      "season": API_SEASON,
                      "game": id,
                      "bookmaker": API_BOOKMAKER,
                      "bet": BETTYPE[0]
                     }
      headers = {
                  "X-RapidAPI-Key": API_KEY,
                  "X-RapidAPI-Host": API_HOST,
                }
      response = requests.get(API_URL['odds'], headers=headers, params=querystring)
      data = response.json()['response']
      home = full_to_abbr[data[0]['game']['teams']['home']['name']]
      away = full_to_abbr[data[0]['game']['teams']['away']['name']]
      hteam.append(home)
      ateam.append(away)
      hodds.append(
        decimal_to_american(data[0]['bookmakers'][0]['bets'][0]['values'][0]['odd'])
      )
      aodds.append(
        decimal_to_american(data[0]['bookmakers'][0]['bets'][0]['values'][1]['odd'])
      )
      filename = f"Json/{date}{home}@{away}.json"
      with open(filename, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, indent=4)
      
      # Get Total
      querystring = { 
                      "league": API_LEAGUE,
                      "season": API_SEASON,
                      "game": id,
                      "bookmaker": API_BOOKMAKER,
                      "bet": BETTYPE[1]
                     }
      response = requests.get(API_URL['odds'], headers=headers, params=querystring)
      data = response.json()['response']
      filename = f"Json/{date}{home}@{away}_OU.json"
      with open(filename, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, indent=4)
      
    df = pd.DataFrame()
    df['Visit'] = ateam
    df['Home'] = hteam
    df['V_Odd'] = aodds
    df['H_Odd'] = hodds
    # df['OU'] = total    
    
    # condition = (df.V_Odd == 0) | (df.H_Odd == 0) | (df.OU == 0)
    # print(f"scraping_odds: SANITIZING DATAFRAME...")
    # debris = df[condition].index
    # df.drop(debris, inplace=True) 
    # df.reset_index(drop=True, inplace=True)
    
    print(df)
    return df

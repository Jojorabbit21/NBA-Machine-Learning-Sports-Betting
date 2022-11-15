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
API_BOOKMAKER = [
  12, # Pinnacle
  3, # 1xbet
  4, # bet365
  19, # Unibet
  26, # Williamhill
]
BETTYPE = [
  2, # 2way
  4  # Ou
]

class Odds():
  remain:int = 0
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
                      "game": int(id),
                      "bet": BETTYPE[0]
                     }
      headers = {
                  "X-RapidAPI-Key": API_KEY,
                  "X-RapidAPI-Host": API_HOST,
                }
      response = requests.get(API_URL['odds'], headers=headers, params=querystring)
      if response.status_code == 200:
        data = response.json()
        try:
          home = full_to_abbr[data['response'][0]['game']['teams']['home']['name']]
          hteam.append(home)
        except:
          hteam.append(0)
          print('no data for {}'.format(id))
        try:
          away = full_to_abbr[data['response'][0]['game']['teams']['away']['name']]
          ateam.append(away)
        except:
          ateam.append(0)
          print('no data for {}'.format(id))
          
        try:
          for bookie in data['response'][0]['bookmakers']:
            if bookie['id'] in API_BOOKMAKER:
              try:
                ho = bookie['bets'][0]['values'][0]['odd']
                hodds.append(decimal_to_american(ho))
              except:
                hodds.append(0)
                print('no home odds for {}'.format(id))
              try:
                ao = bookie['bets'][0]['values'][1]['odd']
                aodds.append(decimal_to_american(ao))
              except:
                aodds.append(0)
                print('no away odds for {}'.format(id))
              break
            
          filename = f"Json/{date}{away}@{home}.json"
          with open(filename, 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4)
        except:
          print('no data for {}'.format(id))
          
        # Get Total
        querystring = { 
                        "league": API_LEAGUE,
                        "season": API_SEASON,
                        "game": id,
                        "bookmaker": API_BOOKMAKER,
                        "bet": BETTYPE[1]
                      }
        response = requests.get(API_URL['odds'], headers=headers, params=querystring)
        if response.status_code == 200:
          data = response.json()
          self.remain = response.headers['x-ratelimit-requests-remaining']
          try:
            for bookie in data['response'][0]['bookmakers']:
              if bookie['id'] in API_BOOKMAKER:
                for bets in bookie['bets'][0]['values']:
                  line = bets['value']
                  odd = float(bets['odd'])
                  if odd >= 1.85 or odd <= 2:
                    line = line.split(" ")[1]
                    total.append(line)
                    break

            filename = f"Json/{date}{away}@{home}_OU.json"
            with open(filename, 'w', encoding='utf-8') as file:
              json.dump(response.json(), file, indent=4)
          except:
            total.append(0)
            print('no total data for {}'.format(id))
          
      else:
        print(response.status_code)
      
    df = pd.DataFrame()
    df['Visit'] = ateam
    df['Home'] = hteam
    df['V_Odd'] = aodds
    df['H_Odd'] = hodds
    df['OU'] = total    
    print(df)
    print('API Quota remain : {}'.format(self.remain))
    # condition = (df.V_Odd == 0) | (df.H_Odd == 0) | (df.OU == 0)
    # print(f"scraping_odds: SANITIZING DATAFRAME...")
    # debris = df[condition].index
    # df.drop(debris, inplace=True) 
    # df.reset_index(drop=True, inplace=True)
    # print(df)
    
    return df

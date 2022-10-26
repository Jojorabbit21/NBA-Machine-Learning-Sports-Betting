import pandas as pd
import csv

team = {
    'Brooklyn': 'BKN',
    'Milwaukee': 'MIL',
    'GoldenState': 'GS',
    'Indiana': 'IND',
    'Charlotte': 'CHA',
    'Chicago': 'CHI',
    'Detroit': 'DET',
    'Washington': 'WAS',
    'Toronto': 'TOR',
    'Boston': 'BOS',
    'NewYork': 'NY',
    'Cleveland': 'CLE',
    'Memphis': 'MEM',
    'Philadelphia': 'PHI',
    'NewOrleans': 'NO',
    'Houston': 'HOU',
    'Minnesota': 'MIN',
    'Orlando': 'ORL',
    'SanAntonio': 'SA',
    'OklahomaCity': 'OKC',
    'Utah': 'UTA',
    'Sacramento': 'SAC',
    'Portland': 'POR',
    'Denver': 'DEN',
    'Phoenix': 'PHO',
    'Dallas': 'DAL',
    'Atlanta': 'ATL',
    'Miami': 'MIA',
    'LAClippers': 'LAC',
    'LALakers': 'LAL'
}

SEASONS = [
  "2021-22",
  "2020-21",
  "2019-20",
  "2018-19"
]

def refine_odds(season):
  path = "./Schedules/nba odds {}.xlsx".format(season)
  df = pd.read_excel(path, header=0, index_col=None)
  dates = []; visits = []; homes = []; scores = []; visit_mls = []; home_mls = []; ous = []
  for i in range(0, len(df), 2):
    date = str(df.at[i,'Date'])
    if len(date) == 4:
      date = season[2:4] + '/' + date[0:2] + '/' + date[2:]
    else:
      date = season[5:] + '/' + date[0:1] + '/' + date[1:]
    visit = team[df.at[i,'Team']]
    home = team[df.at[i+1,'Team']]
    visit_score = df.at[i,'Final']
    home_score = df.at[i+1,'Final']
    score = str(visit_score) + '-' + str(home_score) 
    visit_ml = df.at[i,'ML']
    home_ml = df.at[i+1,'ML']
    if int(df.at[i,'Close']) > 100:
      ou = df.at[i,'Close']
    elif int(df.at[i,'Close']) < 100:
      ou = df.at[i+1,'Close']
    dates.append(date)
    visits.append(visit)
    homes.append(home)
    scores.append(score)
    visit_mls.append(visit_ml)
    home_mls.append(home_ml)
    ous.append(ou)
  df = pd.DataFrame(columns=['Date','Visit','Home','V_Odd','H_Odd','OU','Score'])
  df['Date']=dates
  df['Visit']=visits
  df['Home']=homes
  df['V_Odd']=visit_mls
  df['H_Odd']=home_mls
  df['OU']=ous
  df['Score']=scores
  csv_path = './Schedules/nba_{}.csv'.format(season)
  df.to_csv(csv_path,sep=',')
  print(df)
    
if __name__ == '__main__':
  refine_odds('2021-22')
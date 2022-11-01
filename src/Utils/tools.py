import requests
import pandas as pd
import json

games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}

data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}


def get_json_data(url):
    # print(f"get_json_data: START")
    raw_data = requests.get(url, headers=data_headers)
    raw_data.encoding = 'utf-8'
    # raw_data = str(raw_data.text).strip("'<>() ").replace('\'','\"')
    # print(raw_data)
    # data = json.loads(raw_data)
    print(raw_data.status_code)
    json = raw_data.json()
    # print(f"get_json_data: DONE")
    return json.get('resultSets')


def get_todays_games_json(url):
    raw_data = requests.get(url, headers=games_header)
    json = raw_data.json()
    return json.get('gs').get('g')


def to_data_frame(data):
    # print(f"to_data_frame: START")
    data_list = data[0]
    # print(f"to_data_frame: RETURNING...")
    return pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))

def decimal_to_american(odds):
    odds = float(odds)
    if odds >= 2:
        return int((odds - 1) * 100)
    elif odds < 2:
        return int((-100) / (odds - 1))


# def create_todays_games(input_list):
#     games = []
#     for game in input_list:
#         home = game.get('h')
#         away = game.get('v')
#         home_team = home.get('tc') + ' ' + home.get('tn')
#         away_team = away.get('tc') + ' ' + away.get('tn')
#         games.append([home_team, away_team])
#     return games

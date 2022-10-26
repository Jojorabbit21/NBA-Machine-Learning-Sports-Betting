"""
Predicts NBA scores with regularized matrix factorization.
"""

import pandas as pd

class PredictScore:
    """
    NBA model for predicting final scores.
    Seperate predictions are made for Offensive Rating and Pace, which
        are combined to predict the final score.
    """
    def __init__(self, update=False):
        """
        Attributes:
            urls (list): list of basketball reference URLs of games
                to include in model this needs to be manually updated
            teams (list): list of team canonical abbreviations
            box_urls (list): list of URLs to box scores for games
                included in model
            predictions (pd.DataFrame): DataFrame of predicted score.
                Each entry is the predicted score that the team in the
                index will score against each team in the columns.
                To predict a game, two lookups are required, one for
                each team against the other.

        Args:
            update (bool): If True, update predictions DataFrame by
                rescraping and recomputing all values.  Otherwise,
                just use the cached predictions DataFrame.
        """
        self.update = update
        self.teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE',
                      'DAL', 'DEN', 'HOU', 'DET', 'GSW', 'IND',
                      'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
                      'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
                      'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
        self.predictions = self.get_predictions()

    def get_predictions(self):
        """
        Loads predictions from predictions.csv

        Returns:
            predictions (pd.DataFrame): DataFrame of predictions
        """
        predictions = (pd.read_csv('src/ScorePrediction/predictions_2021.csv')
                       .assign(**{'Unnamed: 0': self.teams})
                       .set_index('Unnamed: 0'))
        predictions.columns = self.teams
        return predictions

    def get_scores(self, team1, team2):
        """
        Prints predicted score of two teams playing against each other.
        Teams can be in any order since home team advantage is not considered.

        Args:
            team1 (str): team1 abbreviation
            team2 (str): team2 abbreviation

        Returns:
            None: Prints score
        """
        team1s = self.predictions.loc[team1][team2]
        team2s = self.predictions.loc[team2][team1]
        return f'{round(int(team1s),0)}-{round(int(team2s),0)}'

# model.get_scores('NOP', 'CHO')
# model.get_scores('SAS', 'IND')
# model.get_scores('CHI', 'WAS')
# model.get_scores('ORL', 'ATL')
# model.get_scores('TOR', 'BRK')
# model.get_scores('BOS', 'MIA')
# model.get_scores('DET', 'NYK')
# model.get_scores('MEM', 'HOU')
# model.get_scores('UTA', 'MIN')
# model.get_scores('DEN', 'GSW')
# model.get_scores('PHO', 'POR')


# from nba_api.stats.static import teams
# from nba_api.stats.endpoints import leaguedashteamstats

# pd.set_option('display.max_columns', 999)

# box = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced', team_id_nullable=1610612737)
# df = box.get_data_frames()[0]
# print(df)


# full_to_abbr = {
#     'Atlanta Hawks': 'ATL',
#     'Boston Celtics': 'BOS',
#     'Brooklyn Nets': 'BRK',
#     'Charlotte Hornets': 'CHO',
#     'Chicago Bulls': 'CHI',
#     'Cleveland Cavaliers': 'CLE',
#     'Dallas Mavericks': 'DAL',
#     'Denver Nuggets': 'DEN',
#     'Detroit Pistons': 'DET',
#     'Golden State Warriors': 'GSW',
#     'Houston Rockets': 'HOU',
#     'Indiana Pacers': 'IND',
#     'Los Angeles Clippers': 'LAC',
#     'Los Angeles Lakers': 'LAL',
#     'Memphis Grizzlies': 'MEM',
#     'Miami Heat': 'MIA',
#     'Milwaukee Bucks': 'MIL',
#     'Minnesota Timberwolves': 'MIN',
#     'New Orleans Pelicans': 'NOP',
#     'New York Knicks': 'NYK',
#     'Oklahoma City Thunder': 'OKC',
#     'Orlando Magic': 'ORL',
#     'Philadelphia 76ers': 'PHI',
#     'Phoenix Suns': 'PHO',
#     'Portland Trail Blazers': 'POR',
#     'Sacramento Kings': 'SAC',
#     'San Antonio Spurs': 'SAS',
#     'Toronto Raptors': 'TOR',
#     'Utah Jazz': 'UTA',
#     'Washington Wizards': 'WAS'
# }

# teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE',
#                       'DAL', 'DEN', 'HOU', 'DET', 'GSW', 'IND',
#                       'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
#                       'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
#                       'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

# def update_df(df, team1, team2, value):
#     old_value = df[team2].loc[team1]
#     if old_value == 0:
#         new_value = float(value)
#     else:
#         new_value = (float(old_value) + float(value)) / 2
#     df[team2].loc[team1] = new_value
#     return df

# def get_poss(team_df, opp_df):
#     TM_FGA = int(team_df.loc['FGA'])
#     TM_FTA = int(team_df.loc['FTA'])
#     TM_ORB = int(team_df.loc['ORB'])
#     TM_DRB = int(team_df.loc['DRB'])
#     TM_FG = int(team_df.loc['FG'])
#     TM_TOV = int(team_df.loc['TOV'])
#     OP_FGA = int(opp_df.loc['FGA'])
#     OP_FTA = int(opp_df.loc['FTA'])
#     OP_ORB = int(opp_df.loc['ORB'])
#     OP_DRB = int(opp_df.loc['DRB'])
#     OP_FG = int(opp_df.loc['FG'])
#     OP_TOV = int(opp_df.loc['TOV'])
    
#     # return 0.96 * (TM_FGA + TM_TOV + 0.44 * TM_FTA - TM_ORB) # Traditional Poss
#     return 0.5 * ((TM_FGA + 0.4 * TM_FTA - 1.07 * (TM_ORB / (TM_ORB + OP_DRB)) * (TM_FGA - TM_FG) + TM_TOV)
#         + (OP_FGA + 0.4 * OP_FTA - 1.07 * (OP_ORB / (OP_ORB + TM_DRB)) * (OP_FGA - OP_FG) + OP_TOV))

# def get_pace(poss, op_poss):
#     return 48 * ((poss + op_poss) / (2 * (240 / 5)))

# df_pace = pd.DataFrame(0, index=teams, columns=teams)
# df_OR = pd.DataFrame(0, index=teams, columns=teams)

# urls = ["http://www.basketball-reference.com/leagues/NBA_2022_games-october.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-november.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-december.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-january.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-february.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-march.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-april.html",
#         "http://www.basketball-reference.com/leagues/NBA_2022_games-may.html"
#         ]
# box_urls = []
# for url in urls:
#     print('****', url)
#     response = ul.urlopen(url)
#     html = response.read()
#     soup = BeautifulSoup(html, 'html.parser')
#     soup.find_all('a')
#     for link in soup.find_all('a'):
#         if link.get('href').startswith('/boxscores/2'):
#             box_urls.append(str(link.get('href')))

# print(len(box_urls))
# for idx, url in enumerate(box_urls):
#     print(f"{idx} game : {url}")
#     url = 'http://www.basketball-reference.com' + url
#     req = requests.get(url)
#     html = req.text
#     soup = BeautifulSoup(html, 'html.parser')
#     home_abbr = soup.select_one('#content > div.scorebox > div:nth-child(2) > div:nth-child(1) > strong > a')
#     away_abbr = soup.select_one('#content > div.scorebox > div:nth-child(1) > div:nth-child(1) > strong > a')
#     home_abbr = full_to_abbr[home_abbr.text]
#     away_abbr = full_to_abbr[away_abbr.text]

#     df = pd.read_html(html)

#     for frame in df:
#         frame.columns = frame.columns.droplevel(0)
#         frame.set_index('Starters', drop=True, inplace=True)

#     # 16 = Reg , 18 = 1OT, 20 = 2OT
#     length = len(df)
#     visitors_basic = df[0].loc['Team Totals', :]
#     visitors_adv = df[int((length / 2) - 1)].loc['Team Totals', :]
#     home_basic = df[int(length / 2)].loc['Team Totals', :]
#     home_adv = df[int(length - 1)].loc['Team Totals', :]

#     v = get_poss(visitors_basic, home_basic)
#     h = get_poss(home_basic, visitors_basic)

#     pace = get_pace(v, h)
#     v_or = visitors_adv['ORtg']
#     h_or = home_adv['ORtg']

#     df_pace = update_df(df_pace, home_abbr, away_abbr, pace)
#     df_pace = update_df(df_pace, away_abbr, home_abbr, pace)
#     df_OR = update_df(df_OR, home_abbr, away_abbr, h_or)
#     df_OR = update_df(df_OR, away_abbr, home_abbr, v_or)
    
#     df_pace.to_csv('pace_2021.csv')
#     df_OR.to_csv('ortg_2021.csv')

import os
import argparse
import pandas as pd

from datetime import datetime, timedelta, timezone
from src.Utils.Dictionaries import team_index_current, team_initials
from src.Utils.tools import get_json_data, to_data_frame

os.environ['CUDA_VISIBLE_DEVICES'] = "-1"

todays_games_url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2022/scores/00_todays_scores.json'
data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2022-23&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='

def createTodaysGames(df, odds, date):
    
    # Visitor,Home,VisitorML,HomeML,UO
    games = []
    match_data = []
    todays_games_uo = []
    home_team_odds = []
    away_team_odds = []

    print(f"create_todays_games: REORGANIZING DATAS...")
    
    for game in range(len(odds)):
        home_team = team_initials[odds.loc[game,'Home']]
        away_team = team_initials[odds.loc[game,'Visit']]
        home_team_odds.append(odds.loc[game,'H_Odd'])
        away_team_odds.append(odds.loc[game,'V_Odd'])
        todays_games_uo.append(odds.loc[game,'OU'])
        home_team_series = df.iloc[team_index_current.get(home_team)]
        away_team_series = df.iloc[team_index_current.get(away_team)]
        # stats = home_team_series.append(away_team_series) -> soon be deprecated series.append
        stats = pd.concat([home_team_series, away_team_series])
        match_data.append(stats)
        games.append([home_team, away_team])     
    print(f"create_todays_games: CREATING DATAFRAME...")
    games_data_frame = pd.concat(match_data, ignore_index=True, axis=1)
    games_data_frame = games_data_frame.T

    print(f"create_todays_games: SANITIZING DATAS...")
    frame_ml = games_data_frame.drop(columns=['TEAM_ID', 'CFID', 'CFPARAMS', 'TEAM_NAME'])
    data = frame_ml.values
    data = data.astype(float)

    return games, data, todays_games_uo, frame_ml, home_team_odds, away_team_odds


def main():
    
    if args.getodds:
        from src.Odds.api import Odds
        fetch = Odds()
        today = datetime.today()
        # today = today + timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        ids = fetch.request_data(today)
        data = fetch.build_data(ids)
    
    if args.creategames:
        from src.ProcessData.Create_Games import create_game
        create_game()
        
    if args.getdata:
        from src.ProcessData.Get_Data import create_data
        create_data(2022,2022)
    
    if args.processodds:
        from src.ProcessData.Process_Odds_Data import create_odds_data
        create_odds_data("2022", "2023")
    
    if args.history | args.tomorrow | args.pergame:
        import tensorflow as tf
        from src.Upload.gs import update_dataframe
        from src.Predict import NN_Runner, XGBoost_Runner
        from src.Scraper.getodds import scrape_odds, scrape_odds_history
        # 지난 경기
        if args.history:
            data = get_json_data(data_url)
            df = to_data_frame(data)
            td = input("Date(YYYY-MM-DD): ")
            target_season = input("Target Season: ")
            odds = pd.read_csv('2022-23.csv')
            games, data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(df, odds, td)
            print("---------------XGBoost Model Predictions---------------")
            result_xd, result_xe = XGBoost_Runner.xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, td)
            result_xdf = pd.DataFrame(result_xd)
            result_xedf = pd.DataFrame(result_xe)
            result_xgb = pd.concat([result_xdf, result_xedf], axis=1)
            print("-------------------------------------------------------")
            data = tf.keras.utils.normalize(data, axis=1)
            print("------------Neural Network Model Predictions-----------")
            result_nd, result_ne = NN_Runner.nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, td)
            result_ndf = pd.DataFrame(result_nd)
            result_nedf = pd.DataFrame(result_ne)
            result_nn = pd.concat([result_ndf, result_nedf], axis=1)
            print("-------------------------------------------------------")
            result = pd.concat([result_xgb, result_nn], axis=0)
            update_dataframe(result, target_season)
        
        # 내일 경기 돌릴때 사용
        if args.tomorrow:
            from src.Odds.api import Odds
            data = get_json_data(data_url)
            df = to_data_frame(data)
            td = datetime.now()
            # est = td - timedelta(hours=14)
            fd = td.strftime('%Y-%m-%d')
            # fd = '2022-10-24'
            target_season = '2022-23'
            odds = scrape_odds(fd)
            games, data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(df, odds, fd)
            print("---------------XGBoost Model Predictions---------------")
            result_xd, result_xe = XGBoost_Runner.xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, fd)
            print(result_xd)
            result_xdf = pd.DataFrame(result_xd)
            result_xedf = pd.DataFrame(result_xe)
            result_xgb = pd.concat([result_xdf, result_xedf], axis=1)
            print("-------------------------------------------------------")
            data = tf.keras.utils.normalize(data, axis=1)
            print("------------Neural Network Model Predictions-----------")
            result_nd, result_ne = NN_Runner.nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, fd)
            result_ndf = pd.DataFrame(result_nd)
            result_nedf = pd.DataFrame(result_ne)
            result_nn = pd.concat([result_ndf, result_nedf], axis=1)
            print("-------------------------------------------------------")
            result = pd.concat([result_xgb, result_nn], axis=0)
            update_dataframe(result, target_season)
        
        if args.pergame:
            data = get_json_data(data_url)
            df = to_data_frame(data)
            td = input("Date(YYYY-MM-DD): ")
            match = []
            match.append(input("Home(Abbr): "))
            match.append(input("Away(Abbr): "))
            match.append(input("Home Moneyline: "))
            match.append(input("Away Moneyline: "))
            match.append(input("Total: "))
            print(match)
            odds = pd.DataFrame([match], columns=['Visit', 'Home', 'V_Odd', 'H_Odd', 'OU'])
            games, data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(df, odds, td)
            print("---------------XGBoost Model Predictions---------------")
            result_xd, result_xe = XGBoost_Runner.xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, td)
            result_xdf = pd.DataFrame(result_xd)
            result_xedf = pd.DataFrame(result_xe)
            result_xgb = pd.concat([result_xdf, result_xedf], axis=1)
            print("-------------------------------------------------------")
            data = tf.keras.utils.normalize(data, axis=1)
            print("------------Neural Network Model Predictions-----------")
            result_nd, result_ne = NN_Runner.nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, td)
            result_ndf = pd.DataFrame(result_nd)
            result_nedf = pd.DataFrame(result_ne)
            result_nn = pd.concat([result_ndf, result_nedf], axis=1)
            print("-------------------------------------------------------")
            result = pd.concat([result_xgb, result_nn], axis=0)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model to Run')
    parser.add_argument('-tomorrow', action='store_true', help='Run Tomorrow matches')
    parser.add_argument('-history', action='store_true', help='Run history matches')
    parser.add_argument('-pergame', action='store_true', help='Run per game prediction')
    parser.add_argument('-processodds', action='store_true', help='Process Odds Data')
    parser.add_argument('-getdata', action='store_true', help='Get Data')
    parser.add_argument('-creategames', action='store_true', help='Create Games')
    parser.add_argument('-getodds', action='store_true', help='Get Odds')
    args = parser.parse_args()
    main()
import copy
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init, deinit
from src.Utils import Expected_Value, Dictionaries
from src.ScorePrediction.model import PredictScore


# from src.Utils.Dictionaries import team_index_current
# from src.Utils.tools import get_json_data, to_data_frame, get_todays_games_json, create_todays_games
init()
xgb_ml = xgb.Booster()
# xgb_ml.load_model('Models/XGBoost_Models/XGBoost_Model.json')
xgb_ml.load_model('Models/XGBoost_Models/XGBoost_79.1%_ML-4.json')
xgb_uo = xgb.Booster()
xgb_uo.load_model('Models/XGBoost_Models/XGBoost_72.3%_UO-7.json')
# xgb_uo.load_model('Models/XGBoost_Models/XGBoost_Model_UO.json')


def xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, date):
    ml_predictions_array = []
    
    result_df = []
    result_ev = []
    result_line = []
    result_ev_line = []
    
    for row in data:
        ml_predictions_array.append(xgb_ml.predict(xgb.DMatrix(np.array([row]))))

    frame_uo = copy.deepcopy(frame_ml)
    frame_uo['OU'] = np.asarray(todays_games_uo)
    data = frame_uo.values
    data = data.astype(float)

    ou_predictions_array = []

    for row in data:
        ou_predictions_array.append(xgb_uo.predict(xgb.DMatrix(np.array([row]))))

    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        winner = int(np.argmax(ml_predictions_array[count]))
        under_over = int(np.argmax(ou_predictions_array[count]))
        winner_confidence = ml_predictions_array[count]
        un_confidence = ou_predictions_array[count]
        
        now = datetime.now()
        now = now + timedelta(hours=12)
        tz = now.strftime("%Y/%m/%d")
        
        result_line.append(tz)
        result_line.append("Xgb")
        result_line.append(away_team)
        result_line.append(home_team)
        
        # Positive odds - 1 plus (the american odds divided by 100) e.g. american odds of 300 = 1 + (300/100) = 4.
        # Negative odds - 1 minus (100 divided by the american odds) e.g. american odds of -300 = 1 - (100/-300) = 1.333
        o = 0.000
        if int(away_team_odds[count]) > 0:
            o = round(1 + (int(away_team_odds[count]) / 100),3)
            result_line.append(o)
        elif int(away_team_odds[count]) < 0:
            o = round(1 - (100 / int(away_team_odds[count])),3)
            result_line.append(o)
        
        if int(home_team_odds[count]) > 0:
            o = round(1 + (int(home_team_odds[count]) / 100),3)
            result_line.append(o)
        elif int(home_team_odds[count]) < 0:
            o = round(1 - (100 / int(home_team_odds[count])),3)
            result_line.append(o)        

        result_line.append(round(winner_confidence[0][0] * 100, 1))
        result_line.append(round(winner_confidence[0][1] * 100, 1))
        result_line.append(todays_games_uo[count])
        
        predict_exact_score = PredictScore(update=False)
        exact_score = predict_exact_score.get_scores(Dictionaries.team_index_bref[away_team], Dictionaries.team_index_bref[home_team])
        score = ""
        confidence = 0
        
        if winner == 1:
            winner_confidence = round(winner_confidence[0][1] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(
                    Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                    Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(
                        todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
                score = "UNDER"
                confidence = un_confidence    
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(
                    Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                    Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(
                        todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
                score = "OVER"
                confidence = un_confidence  
        else:
            winner_confidence = round(winner_confidence[0][0] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(
                    Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                    Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(
                        todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
                score = "UNDER"
                confidence = un_confidence  
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(
                    Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                    Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(
                        todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
                score = "OVER"
                confidence = un_confidence  
        result_line.append(score)
        result_line.append(exact_score)
        result_line.append(confidence)
        result_df.append(result_line)
        result_line = []
        count += 1
    print("--------------------Expected Value---------------------")
    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        ev_home = float(Expected_Value.get_ev(ml_predictions_array[count][0][1], int(home_team_odds[count])))
        ev_away = float(Expected_Value.get_ev(ml_predictions_array[count][0][0], int(away_team_odds[count])))
        if ev_home > 0:
            print(home_team + ' EV: ' + Fore.GREEN + str(ev_home) + Style.RESET_ALL)
        else:
            print(home_team + ' EV: ' + Fore.RED + str(ev_home) + Style.RESET_ALL)

        if ev_away > 0:
            print(away_team + ' EV: ' + Fore.GREEN + str(ev_away) + Style.RESET_ALL)
        else:
            print(away_team + ' EV: ' + Fore.RED + str(ev_away) + Style.RESET_ALL)
        result_ev_line.append(ev_away)
        result_ev_line.append(ev_home)
        result_ev.append(result_ev_line)
        result_ev_line = []
        count += 1

    deinit()
    return result_df, result_ev

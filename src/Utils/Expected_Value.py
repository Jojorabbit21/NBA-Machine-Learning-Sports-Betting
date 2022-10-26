def expected_value(Pwin, odds):
    # example) Pwin, odds = 0.39653975 -130
    Ploss = 1 - Pwin
    # ex) 0.6034602522850037
    Mwin = payout(odds)
    # Mwin = 76.9230....
    
    return round((Pwin * Mwin) - (Ploss * 100), 2)
    # (46.9230) - (60.34)

def payout(odds):
    # ex) -130
    if odds > 0:
        return odds
    # 100 / (-1 * -130)) * 100 = 76.9230...
    return (100 / (-1 * odds)) * 100

def get_ev(win_probability, odds):
    wage = 10
    odds = convert_odds(int(odds))
    return (((odds * wage) - wage) * win_probability) - (wage * (1 - win_probability))

def convert_odds(odds):
    if odds > 0:
        return round(1 + (odds / 100), 2)
    else:
        return round(1 - (100 / odds), 2)
import os

from tqdm import tqdm

from src.Utils.tools import get_json_data, to_data_frame

url = 'https://stats.nba.com/stats/' \
      'leaguedashteamstats?Conference=&' \
      'DateFrom=10%2F1%2F{}&DateTo={}%2F{}%2F{}' \
      '&Division=&GameScope=&GameSegment=&LastNGames=0&' \
      'LeagueID=00&Location=&MeasureType=Base&Month=0&' \
      'OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&' \
      'PerMode=PerGame&Period=0&PlayerExperience=&' \
      'PlayerPosition=&PlusMinus=N&Rank=N&' \
      'Season={}' \
      '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
      'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='

year = [
    2007,
    2008, 
    2009, 
    2010, 
    2011, 
    2012, 
    2013, 
    2014, 
    2015, 
    2016, 
    2017, 
    2018, 
    2019, 
    2020, 
    2021, 
    2022,
    2023
    ]
season = [
    "2007-08", 
    "2008-09", 
    "2009-10", 
    "2010-11", 
    "2011-12", 
    "2012-13", 
    "2013-14", 
    "2014-15", 
    "2015-16", 
    "2016-17",
    "2017-18", 
    "2018-19",
    "2019-20",
    "2020-21", 
    "2021-22",
    "2022-23"
    ]
month = [10, 11, 12, 1, 2, 3, 4, 5, 6]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

def create_data(start_season:int, end_season:int=None):
    
    begin_year_pointer = start_season
    if end_season == None:
        end_year_pointer = start_season + 1
    if end_season == start_season:
        end_year_pointer = start_season + 1
    else:
        end_year_pointer = end_season
    seasons = []
    for i in range(begin_year_pointer, end_year_pointer+1):
        seasons.append(i)

    for season1 in seasons:
        suffix = int(str(season1)[-2:])+1
        full_season = str(season1) + "-" + str(suffix)
        print(full_season)
        
        if not os.path.isdir(f'TeamData/{full_season}'):
            os.mkdir(f'TeamData/{full_season}')
            print(f'{full_season} folder created')
            
        year_from = season1
        year_current = season1
        for month1 in month:
            if month1 == 1:
                year_current += 1
            for day1 in days:
                
                if os.path.isfile(f'TeamData/{full_season}/{month1}-{day1}-{year_current}.xlsx'):
                    print(f'data already exists on {month1}/{day1}/{year_current}')
                    continue
                else:
                    target_month = month1
                    target_day = day1
                    data_url = url.format(
                                int(year_from), 
                                int(target_month),
                                int(target_day),
                                int(year_current),
                                full_season)
                        
                    try:
                        general_data = get_json_data(data_url)
                        general_df = to_data_frame(general_data)
                        general_df['Date'] = str(target_month) + '-' + str(target_day) + '-' + str(full_season)
                        
                        if not general_df.empty:
                            directory2 = os.fsdecode(f'TeamData/{full_season}')
                            name = directory2 + '/' + str(target_month) + '-' + str(target_day) + '-' + str(full_season) + '.xlsx'
                            general_df.to_excel(name)
                            print(f'{target_month}/{target_day}/{full_season}.xlsx created')
                        else:
                            print(f'no data on {target_month}/{target_day}/{full_season}')
                    except:
                        print(f"data fetching error {target_month}/{target_day}/{full_season}")
                        pass
                    
        begin_year_pointer += 1

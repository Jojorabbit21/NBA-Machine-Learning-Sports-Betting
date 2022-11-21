# -*- coding: utf-8 -*-
import pandas as pd
import os.path

from src.Utils.Dictionaries import team_rotowire
from datetime import datetime
from pytz import timezone
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def scrape_odds(date):
    
    url = 'https://www.rotowire.com/betting/nba/odds?date=' + date
    print(f"scraping_odds: {url}")
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('disable-gpu')
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options, executable_path=r'./src/Scraper/chromedriver.exe')
    
    print(f"scraping_odds: OPENING BROWSER")
    driver.get(url)
    driver.implicitly_wait(2)
    sleep(2)

    visit = []
    home = []
    visit_odds = []
    home_odds = []
    ou = []
    
    # Team Name Selector
    # div.webix_ss_body > div.webix_ss_left > div > div > div:nth-child(1) > a > span.hide-until-md
    # Moneyline Odds Selector
    # div.webix_ss_body > div.webix_ss_center > div > div:nth-child(2)
    
    print(f"scraping_odds: FETCHING TEAMS...")
    teams = driver.find_elements(By.CSS_SELECTOR, 'div.webix_ss_body > div.webix_ss_left > div > div > div > a > span.hide-until-md')
    for i in range(len(teams)):
        if i%2==0:
            visit.append(team_rotowire[teams[i].text])
        else:
            home.append(team_rotowire[teams[i].text])
        
    print(f"scraping_odds: FETCHING MONEYLINE...")
    moneyline = driver.find_elements(By.CSS_SELECTOR, 'div.webix_ss_body > div.webix_ss_center > div > div:nth-child(2) > div')
    for i in range(len(moneyline)):
        if i%2==0:
            if moneyline[i].text != '-':
                visit_odds.append(moneyline[i].text)
            else:
                visit_odds.append(0)
        else:
            if moneyline[i].text != '-':
                home_odds.append(moneyline[i].text)
            else:
                home_odds.append(0)
    
    print(f"scraping_odds: FETCHING UNDER/OVER ODDS...")
    ouodds = driver.find_elements(By.CSS_SELECTOR, 'div.webix_ss_body > div.webix_ss_center > div > div:nth-child(6) > div')
    for i in range(len(ouodds)):
        if i%2 == 0:
            if ouodds[i].text != '-':
                val = str(ouodds[i].text)
                ou.append(val[2:])
            else:
                ou.append(0)
           
    driver.close()
    
    print(f"scraping_odds: BUILDING DATAFRAME...")
   
    df = pd.DataFrame()
    df["Visit"] = visit
    df['Home'] = home
    df['V_Odd'] = visit_odds
    df['H_Odd'] = home_odds
    df['OU'] = ou
    
    print(f"scraping_odds: SANITIZING DATAFRAME...")
    condition = (df.V_Odd == 0) | (df.H_Odd == 0) | (df.OU == 0)
    debris = df[condition].index
    df.drop(debris, inplace=True) 
    df.reset_index(drop=True, inplace=True)
    
    df.to_csv('history.csv', mode='a', header=False, index=False)
    
    print(f"scraping_odds: DONE...")
    print(df)
    return df

def scrape_odds_history(season:str='2020-21'):
    path = './Schedules/nba_{}.csv'.format(season)
    df = pd.read_csv(path,header=0)
    df = df.loc[:,['Visit','Home','V_Odd','H_Odd','OU']]
    return df
    

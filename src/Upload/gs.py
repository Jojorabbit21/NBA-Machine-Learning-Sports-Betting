import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe

def update_dataframe(df, sheet):
    gc = gspread.service_account(filename="./src/Upload/agent.json")
    sh = gc.open("NBA ML").worksheet(sheet)
    last_row = int(sh.acell('A1').value) + 1
    set_with_dataframe(sh,df,last_row,2,include_index=False,include_column_header=False)
    
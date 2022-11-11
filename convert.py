import pandas as pd
from src.Utils.tools import decimal_to_american

df = pd.read_csv('2022-23_betman.csv')

vo = []
ho = []

for row in df.itertuples():
  vo.append(decimal_to_american(row[4]))
  ho.append(decimal_to_american(row[5]))
  
df['V_Odd'] = vo
df['H_Odd'] = ho

df.to_csv('2022-23_betman_cleaned.csv')
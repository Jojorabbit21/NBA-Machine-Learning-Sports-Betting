import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from tqdm import tqdm
import numpy as np


data = pd.read_excel('./Datasets/Full-Data-Set-UnderOver-2020-2023.xlsx')
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'],
          axis=1, inplace=True)
data = data.values
data = data.astype(float)

# classfier = RandomForestClassifier(n_estimators = 100)

# for x in tqdm(range(100)):

for x in tqdm(range(100)):
  x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=.1)

  rand_clf = RandomForestClassifier(criterion='entropy', bootstrap=True, random_state=42, max_depth=5)
  rand_clf.fit(x_train, y_train)
  y_pred = rand_clf.predict(x_test)

  print('train acc: {: .3f}'.format(rand_clf.score(x_train, y_train)))
  print('test acc: {: .3f}'.format(rand_clf.score(x_test, y_test)))
  
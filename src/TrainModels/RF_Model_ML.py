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

x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=.1)

cv = KFold(n_splits=5)
accuracies = list()
max_attributes = x_test.shape[1]
depth_range = range(1, max_attributes)

for depth in depth_range:
  fold_accuracy = []
  rand_clf = RandomForestClassifier(max_depth=depth)
  for train_fold, valid_fold in cv.split(x_train):
    
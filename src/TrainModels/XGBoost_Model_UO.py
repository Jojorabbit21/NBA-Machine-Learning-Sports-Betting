import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from tqdm import tqdm
import numpy as np

data = pd.read_excel('./Datasets/Full-Data-Set-UnderOver-2021-22.xlsx')
OU = data['OU-Cover']
data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover'], axis=1,
          inplace=True)
data = data.values
data = data.astype(float)

# ** Finding best parameters by GridSearchCV

# x_train, x_test, y_train, y_test = train_test_split(data, OU, test_size=.1)
# params = {
#     'max_depth': [3, 5, 7, 10],
#     'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5],
#     'gamma': [0, 1, 2],
#     'min_child_weight': [1, 3, 6, 10],
#     'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1],
# }

# from xgboost import XGBClassifier
# xgb = XGBClassifier()
# gscv_xgb = GridSearchCV(estimator = xgb, param_grid = params, scoring ='accuracy', cv = 5, refit=True, n_jobs=-1, verbose=2)
# gscv_xgb.fit(x_train, y_train)

# print("="*30)
# print("XGB Parameters: ", gscv_xgb.best_params_)
# print('XGB Accuracy: {:.4f}'.format(gscv_xgb.best_score_))
# print("="*30)

for x in tqdm(range(100)):
    x_train, x_test, y_train, y_test = train_test_split(data, OU, test_size=.1)

    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)

    param = {
        'max_depth': 3,
        'colsample_bytree': 1,
        'min_child_weight': 10,
        'gamma': 1,
        'eta': 0.05,
        'eval_metric': 'logloss',
        'objective': 'multi:softprob',
        'num_class': 3,
    }
    # param = { #UO-7
    #     'booster': 'gbtree',
    #     'max_depth': 6,
    #     'min_child_weight': 3,
    #     'gamma': 1,
    #     'eta': 0.01,
    #     'objective': 'multi:softprob',
    #     'num_class': 3,
    #     'eval_metric': 'logloss'
    # }
    epochs = 500

    model = xgb.train(param, train, num_boost_round=epochs)
    predictions = model.predict(test)
    y = []

    for z in predictions:
        y.append(np.argmax(z))

    acc = round(accuracy_score(y_test, y), 3) * 100
    print(acc)
    model.save_model('./Models/XGBoost_UO-8_{}.json'.format(acc))

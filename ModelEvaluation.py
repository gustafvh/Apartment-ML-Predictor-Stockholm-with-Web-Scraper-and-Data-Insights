import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.metrics import accuracy_score


from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor


# From Kaggle
def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = RandomForestRegressor(
        max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)


def tryParameters(trainFeatures, valFeatures, trainPredictionTarget, valPredictionTarget):

        # compare MAE with differing values of max_leaf_nodes
    for max_leaf_nodes in [5, 50, 500, 5000, 10000, 500000, 100000]:
        my_mae = get_mae(max_leaf_nodes, trainFeatures, valFeatures,
                         trainPredictionTarget, valPredictionTarget)
        print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %
              (max_leaf_nodes, my_mae))

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.metrics import accuracy_score


def getPredictions(df, features, target):
    # Y
    target = df[target]
    # X

    df = df[features]

    trainFeatures, valFeatures, trainPredictionTarget, valPredictionTarget = train_test_split(
        df, target, random_state=0)

    trainedModel = RandomForestRegressor(
        random_state=1)

    trainedModel.fit(trainFeatures, trainPredictionTarget)

    modelPredictions = trainedModel.predict(
        valFeatures)

    return modelPredictions, valPredictionTarget, trainedModel

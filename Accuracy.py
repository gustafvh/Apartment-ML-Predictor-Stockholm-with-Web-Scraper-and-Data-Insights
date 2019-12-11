from sklearn.metrics import mean_absolute_error, accuracy_score
import numpy as np


def printMeanAbsoluteError(predictions, valPredictionTarget):

    mae_error = mean_absolute_error(valPredictionTarget, predictions)
    mae_error = round(mae_error, 0)
    mae_error = '{:,.2f}'.format(mae_error)

    print("Predictions for", len(predictions), "apartments are off (MAE) by:")
    print(mae_error, "SEK")


def printMeanAbsolutePercentageError(valPredictionTarget, predictions):
    valPredictionTarget, predictions = np.array(
        valPredictionTarget), np.array(predictions)
    maeP = np.mean(
        np.abs((valPredictionTarget - predictions) / valPredictionTarget)) * 100
    maeP = round(maeP, 2)
    print("Predictions for", len(predictions), "apartments are off (MAPE) by:")
    print(maeP, "%")

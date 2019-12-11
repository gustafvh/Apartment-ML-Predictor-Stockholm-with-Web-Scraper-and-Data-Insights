import pandas as pd
import numpy as np
from WebCrawler.WebCrawler import *
from ProcessData import cleanAndConvertToNum
from YelpApi import updateDfWithYelpDetails
from VisualizeData import showBarChart, showHeatMap, showScatterPlotLine
from Model import getPredictions
from Accuracy import printMeanAbsoluteError, printMeanAbsolutePercentageError

import time


def getRowsFromHnet(driver, numberOfPages):
    # One page is 50 rows
    # driver = initCrawler(20, 25)

    apData = pd.DataFrame()
    apData = getMultiplePages(driver, numberOfPages)

    return apData


def writeToCsv(dataframe):
    dataframe.to_csv('hnetData.csv', index=False)


def getAllSegments():
    apData = pd.DataFrame()
    segments = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65,
                70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 250]

    for i in range(0, (len(segments)-1)):
        driver = initCrawler(segments[i], segments[i+1])
        apDataNew = getRowsFromHnet(driver, 50)
        apData = apData.append(apDataNew, ignore_index=True)

    return apData


def createYelpData():
    apData = pd.read_csv('./Data/hnetData.csv')

    apData = cleanAndConvertToNum(apData)

    # creates file named 'yelpDataX-Y.csv'
    apData = updateDfWithYelpDetails(apData, 0, 4000)


def cleanData():
    apData = pd.read_csv('./Data/hnetData.csv')

    apData = cleanAndConvertToNum(apData)

    apData.to_csv('./Data/CleanHnetData.csv', index=False)


def main():

    # Step 1 - Get all data from hNet
    # getAllSegments()

    # Step 2 - Clean data with formatting and output to new csv file
    # cleanData()

    # Step 3 - Read CSV and make import and add Yelp Data
    apData = pd.read_csv('./Data/CleanHnetData.csv')
    #apData = updateDfWithYelpDetails(apData, 0, 4000)

    # Step 4 - Read final datafile, and use as dataframe

    # Step 5 - Get a trained model based on dataframe
    featuresToTrainOn = ['Date', 'Size', 'Rooms']
    target = 'Price'
    numOfPredictions = 10

    # Predictions is array with predictions
    predictions, valPredictionTarget, model = getPredictions(
        apData, featuresToTrainOn, target)

    printMeanAbsoluteError(predictions, valPredictionTarget)
    printMeanAbsolutePercentageError(predictions, valPredictionTarget)

    #############################################

    #showBarChart(apData.head(1000), 'Price')
    #showScatterPlotLine(apData, 'Size', 'Price')

    # print(apData.info())
    # print(apData.head(10))


main()
# createYelpData()

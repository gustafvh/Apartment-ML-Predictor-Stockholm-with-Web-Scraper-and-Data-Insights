import pandas as pd
import numpy as np

from mpl_toolkits.mplot3d import Axes3D


from WebScraper.WebScraper import *
from ProcessData import cleanAndConvertToNum, removeOutliers, removeWrongCoordinates, addPricePerSizeColumn
from YelpApi import updateDfWithYelpDetails
from VisualizeData import showBarChart, showHeatMap, showScatterPlotLine, plotPredictionsTowardsActual, plotThreeDimensionsGraph, plot3DWireframe
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


def preProcess():
    # Step 1.1 - Get all data from hNet
    getAllSegments()

    # Step 1.2 - Clean data with formatting and output to new csv file
    cleanData()

    # Step 1.3 - Read CSV and make import and add Yelp Data
    apData = pd.read_csv('./Data/CleanApData.csv')
    apData = updateDfWithYelpDetails(apData, 13725, 14210)

    # Step 1.4 - Include all rows with column value within X % of data and above Y value
    apData = removeOutliers(apData, 0.80, 0, 'Price')
    apData = removeOutliers(apData, 0.80, 100, 'Rent')

    # Step 1.5 - Read final datafile, and use as dataframe
    apData = pd.read_csv('./yelpDataGather.csv')

    # Step 1.6 - Add PricePerKvm Column
    apData = addPricePerSizeColumn(apData, 0, 14222)

    # Step 1.7 - Remove coordinates that are outside Stockholms municipal
    apData = removeWrongCoordinates(apData)


def main():

    # Step 1 - Run preProcess who gets, cleans, and processes data used. Outputs file FilteredApData.csv
    #
    # preProcess()

    # Step 2 - Read final datafile, and use as dataframe
    apData = pd.read_csv('./Data/FilteredApData.csv')

    # Step 3 - Get a trained model based on dataframe
    featuresToTrainOn = ['Date', 'Size', 'Rooms']
    target = 'Price'

    # Predictions is array with predictions
    predictions, valPredictionTarget, model = getPredictions(
        apData, featuresToTrainOn, target)

    # Step 4 - Print predictions accuracy
    printMeanAbsoluteError(predictions, valPredictionTarget)
    printMeanAbsolutePercentageError(predictions, valPredictionTarget)

    # Step 5 - Visualize output data

    # plotThreeDimensionsGraph(
    #    apData[['Latitude', 'Longitude', 'PricePerKvm']])
    #plot3DWireframe(apData[['Latitude', 'Longitude', 'PricePerKvm']])

    #plotPredictionsTowardsActual(valPredictionTarget, predictions)
    print(apData.head(10))


main()

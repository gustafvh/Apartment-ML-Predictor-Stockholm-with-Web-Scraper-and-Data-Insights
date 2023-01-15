import pandas as pd
from WebScraper.WebScraper import *
from ProcessData import cleanAndConvertToNum

def getRowsFromHnet(driver, numberOfPages):
    # One page is 50 rows
    # driver = initCrawler(20, 25)

    apData = pd.DataFrame()
    apData = getMultiplePages(driver, numberOfPages)

    return apData


def writeToCsv(dataframe):
    dataframe.to_csv('./Data/hnetData.csv', index=False)


def getAllSegments():
    apData = pd.DataFrame()
    # segments = [20, 25] #For testing
    segments = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65,
                70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 250]

    for i in range(0, (len(segments)-1)):
        driver = initCrawler(segments[i], segments[i+1])
        apDataNew = getRowsFromHnet(driver, 50)
        apData = apData.append(apDataNew, ignore_index=True)
    writeToCsv(apData)
    return apData


def cleanData():
    apData = pd.read_csv('./Data/hnetData.csv')
    apData = cleanAndConvertToNum(apData)
    apData.to_csv('./Data/RawDataFile.csv', index=False)

def preProcess():
    # Step 1.1 - Get all data from hNet
    getAllSegments()

    # Step 1.2 - Clean data with formatting and output to new csv file
    cleanData()

def main():

    # Run an initial preProcess which gets, cleans & adds geocoding
    preProcess()

main()

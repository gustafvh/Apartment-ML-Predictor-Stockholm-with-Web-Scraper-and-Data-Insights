import pandas as pd
import numpy as np
from WebCrawler.WebCrawler import *

import time


def getRowsFromHnet(driver, numberOfPages):
    # One page is 50 rows
    #driver = initCrawler(20, 25)

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


def main():
    apData = pd.read_csv('./Data/hnetData.csv')

    # apD = pd.DataFrame()
    # # apData = apData.astype('float')
    # apD = getAllSegments()

    #apData = apData[apData.duplicated(keep=False)]
    print(apData.info())
    # writeToCsv(apD)


main()

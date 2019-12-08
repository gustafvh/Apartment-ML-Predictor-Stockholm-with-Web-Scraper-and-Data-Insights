import pandas as pd
import numpy as np
from WebCrawler.WebCrawler import *

import time


def getRowsFromHnet(numberOfPages):
    # One page is 50 rows
    driver = initCrawler()

    apData = pd.DataFrame()
    apData = getMultiplePages(driver, numberOfPages)

    return apData


def writeToCsv(dataframe):
    dataframe.to_csv('hnetData.csv', index=False)


def main():
    apData = getRowsFromHnet(10)
    print(apData)
    writeToCsv(apData)


main()

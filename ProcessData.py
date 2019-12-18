import pandas as pd
import numpy as np


def cleanAndConvertToNum(df):

    # 6 december 2019 --> 2019 december 6
    df.Date = [apartment.split(' ')[2] + (apartment.split(' ')[1]) + (apartment.split(' ')[0])
               for apartment in df.Date]

    # 24,7 --> 24.7 to help ease float conversion
    df.Size = [size.replace(',', '.')
               for size in df.Size]

    # Remove all floors embedded in Adress ex. ", 3 tr"
    df.Adress = [adress.split(',')[0]
                 for adress in df.Adress]

    # Drop all rows where we have empty/unknown values
    df = df.drop(df[df.Rooms == 'Unknown'].index)
    df = df.drop(df[df.Rent == 'Unknown'].index)

    # Make Date numerical
    df.Date = [date
               .replace('januari', '01')
               .replace('februari', '02')
               .replace('mars', '03')
               .replace('april', '04')
               .replace('maj', '05')
               .replace('juni', '06')
               .replace('juli', '07')
               .replace('augusti', '08')
               .replace('september', '09')
               .replace('oktober', '10')
               .replace('november', '11')
               .replace('december', '12')
               for date in df.Date]

    cols = ['Date', 'Size', 'Rooms', 'Rent', 'Price']
    df[cols] = df[cols].apply(
        pd.to_numeric, errors='coerce', axis=1)

    print(df.info())
    print(df.head(10))

    return df


def getSplitData(dataframe, predictionTarget):

    trainFeatures, valFeatures, trainPredictionTarget, valPredictionTarget = train_test_split(
        dataframe, predictionTarget, random_state=0)

    return trainFeatures, valFeatures, trainPredictionTarget, valPredictionTarget


def removeOutliers(
        df, tolerance, minNum, column):
     # Remove all outliers
    quant = df[column].quantile(tolerance)
    df = df[df[column] < quant]
    df = df[df[column] > minNum]

    return df


def removeWrongCoordinates(df):

    rowCount = len(df.index)
    # Only show rows close to Stockholms coordinates. Yelp might have returned a completely different location
    df = df.loc[df['Longitude'] > 17.6]
    df = df.loc[df['Longitude'] < 18.3]
    df = df.loc[df['Latitude'] < 59.45]
    df = df.loc[df['Latitude'] > 59.2]

    print("removeWrongCoordinates removed",
          rowCount - len(df.index), "rows from apData")

    return df


def addPricePerSizeColumn(df, fromRow, toRow):

    df['PricePerKvm'] = 0.0

    for i in range(fromRow, toRow):
        #df.to_csv(name, index=False)

        df.at[i, 'PricePerKvm'] = round(
            df.at[i, 'Price'] / df.at[i, 'Size'], 0)

    df['PricePerKvm'] = df['PricePerKvm'].astype('float')

    return df

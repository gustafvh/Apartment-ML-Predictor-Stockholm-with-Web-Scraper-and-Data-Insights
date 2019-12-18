# https://www.yelp.com/developers/documentation/v3/business_search

from yelpapi import YelpAPI


def getDetailsFromAdress(adress):
    #adress = adress + " stockholm"
    yelp_api = YelpAPI(
        "MrRGPpo52MhH9Rhd2mYhqVTHUTolmcqQ1ekyXhAdh15ckOCdKeEPqgMvvOCBQM149OD5CpXMlg32NRseNdbtARSn_wErkvnAaLUXwZ0EBm4uhJXucT1ULSSrX9vwXXYx")
    response = yelp_api.search_query(location=adress, radius=2000, limit=1)
    # print(response)
    latitude = response['region']['center']['latitude']
    longitude = response['region']['center']['longitude']
    pointsOfInterestsNearby = response['total']
    return (latitude, longitude, pointsOfInterestsNearby)


def updateDfWithYelpDetails(df, fromRow, toRow):

    # Add columns for NearbyPOIs, Latitude and Longitude
    df['NearbyPOIs'] = 0.0
    df['Latitude'] = 0.0
    df['Longitude'] = 0.0

    name = 'yelpData' + str(fromRow) + "-" + str(toRow) + ".csv"

    df = df.reset_index(drop=True)

    for i in range(fromRow, toRow):
        df.to_csv(name, index=False)
        adress = df.at[i, 'Adress']
        print('Getting Yelp details for', adress, 'on row', i)

        yelpResponse = getDetailsFromAdress(adress)

        df.at[i, 'Latitude'] = yelpResponse[0]
        df.at[i, 'Longitude'] = yelpResponse[1]
        df.at[i, 'NearbyPOIs'] = yelpResponse[2]

    df['NearbyPOIs'] = df['NearbyPOIs'].astype('float')

import numpy as np
import pandas as pd
import seaborn as sns


def createDataframe(apColumns):

    # print(len(apColumns[0]))
    # print(len(apColumns[1]))
    # print(len(apColumns[2]))
    # print(len(apColumns[3]))
    # print(len(apColumns[4]))
    # print(len(apColumns[5]))
    # print(len(apColumns[6]))
    # print(len(apColumns[7]))

    apColumns = {
        'Date': apColumns[0],
        'Area': apColumns[1],
        'Adress': apColumns[2],
        'Size': apColumns[3],
        'Rooms': apColumns[4],
        'Broker': apColumns[5],
        'Rent': apColumns[6],
        'Price': apColumns[7],
    }

    #apDf = pd.DataFrame(data=apColumns)

    # return apDf

import numpy as np
import pandas as pd
import seaborn as sns


def createDataframe(apColumns):

    print(len(apColumns[0]))
    print(len(apColumns[1]))
    print(len(apColumns[2]))
    print(len(apColumns[3]))
    print(len(apColumns[4]))
    print(len(apColumns[5]))
    print(len(apColumns[6]))

    apColumns = {
        'Date': apColumns[0],
        'Adress': apColumns[1],
        'Size': apColumns[2],
        'Rooms': apColumns[3],
        'Broker': apColumns[4],
        'Rent': apColumns[5],
        'Price': apColumns[6],
    }

    apDf = pd.DataFrame(data=apColumns)

    return apDf

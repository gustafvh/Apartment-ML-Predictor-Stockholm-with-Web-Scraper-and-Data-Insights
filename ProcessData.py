import pandas as pd
import numpy as np

apData = pd.read_csv('./Data/hnetData.csv')

apData = apData.astype('float')
print(apData.info())

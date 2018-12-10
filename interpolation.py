import pandas as pd 
import matplotlib
from pandas import read_csv
series=read_csv('newdata.csv' , header =0,index_col=0 , squeeze =True)
interpolated=series.interpolate(methods='linear')
print(interpolated.head(32))
interpolated.to_csv('outsample.csv')
import matplotlib.pyplot as plt
interpolated.plot(figsize=(15,6))
plt.show()

import pyvisa
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

#Filepath where the point the test datafile exists in so it can be accessed
filepath = "C:/Users/TXB909/Documents/strain-cell/"
file = "Cu_py_5k_max_strain_test_200to_neg_200V.csv"

FILEANDPATH=filepath+file

Labels = ['Capacitance(pF)','Loss (nSiemens)','Timestamp (24hr)']
#print(FILEANDPATH)


#The filetypes from a PPMS cryostat have a huge amount of non delimeted information at the start, this throws an error when 
#accessed using the csv pandas function so this try and except loop finds the headers as they are in csv format 

for i in range(100):
    try:
        df_raw_data = pd.read_csv(FILEANDPATH, sep=",", skiprows=i)
        print("headers start on line", i,)
        #make a note of when headers start, need to +1 as we will skip this many rows later and the first one that works is 
        # found not to format the columns correctly
        index_of_headers = int(i)# NB THIS HAS CHANGED COMPARED TO MPMS PLOTTING CODE FROM i+1 to i to include headers
        break
    except:
        None
        #print("headers don't start on line", i,)
    


#new dataframe using the index for headers we found
df_raw_data = pd.read_csv(FILEANDPATH, sep=",", skiprows= index_of_headers)


#drop any rows containing all NaN's as these are not useful, we use 'all' not 'any' as most columns have at least 1 NaN
df_sanitised_once_data = df_raw_data.dropna(axis = 1, how = 'all', inplace = False)


#convert timestamp into seconds to plot
def get_seconds(time_str):
    
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

df_sanitised_once_data['Timestamp (24hr)'] = df_sanitised_once_data['Timestamp (24hr)'].apply(get_seconds)

#now rename column header and the change is complete
df_sanitised_once_data.rename(columns={'Timestamp (24hr)': 'Timestamp(seconds)'}, inplace=True)

print(df_sanitised_once_data)

def plot_data(df, x_column_title, y_column_title, title):
    x = df.loc[:,x_column_title]
    y = df.loc[:,y_column_title]
    fig = figure(figsize=(18,10))

    plt.scatter(x, y, s=10, 
                #c='r', 
                  facecolors='none', edgecolors= 'b', label = 'Data Points')
    plt.plot(x, y, c='r', linewidth=0.8)
    plt.title(title)
    plt.xlabel(x_column_title)
    plt.ylabel(y_column_title)
    plt.grid('both')
    plt.legend()
    plt.show()


plot_data(df_sanitised_once_data,'Timestamp(seconds)' ,'Capacitance(pF)', 'test cap plot')


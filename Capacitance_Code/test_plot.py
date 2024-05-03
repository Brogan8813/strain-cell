'''THIS UPDATES A NEW PLOT AFTER EACH ITERATION, it will work okay'''
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from datetime import date

# Create an empty DataFrame
header = ['Capacitance(pF)','Loss (nSiemens)', 'Timestamp (s)']
df =pd.DataFrame(columns=header)

# Define the number of iterations
num_measurements = 10

# Initialize the plot
plt.figure()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Plot')

# Plotting the initial empty data
plt.plot([], [], marker='o', color='b')

# Display the plot
plt.show(block=False)




start_time = time.time()
no_of_iterations = 10
for i in range(no_of_iterations):
    data_trans = []
        #AH_2550.write('single')
        #time.sleep(0.1)#waits as the AH is slow at times to do measurements 
        #raw_data = AH_2550.read_raw()
        #split_data = raw_data.split()#splits data at every whitespace, can then index through each split string
    timestamp = time.time()-start_time
        #try:
            #data_trans = [float(split_data[1]), float(split_data[3]), round(timestamp, 3)]#select string's that are cap and loss and make them floats
        #except:
            #data_trans = ['NaN', 'NaN', round(timestamp, 3)]#if data cannot be converted to float this can happens when a value isn't produced by the AH2550 and instead 'PF' and 'NS'
        #are then the 1st and 3rd index, this is useless data and if it occurs frequently then the time.sleep(x) after writing may need changing
    
    #comment out the below line, it is for testing with  fake data and timestamp
    data_trans = [float(np.random.randint(1,1000)), float(np.random.randint(1,1000)), round(timestamp, 3)]


    print(data_trans)
    df.loc[i] = data_trans
    plt.plot(df['Timestamp (s)'],df['Capacitance(pF)'], marker='o', color='b')
    plt.ylabel('Capacitance(pF)')
    plt.xlabel('Timestamp (s)')
    plt.title('Data Plot')
    
    # Pause briefly to update the plot
    plt.pause(0.1)  # Adjust pause time as needed
    if i==(no_of_iterations-1):
        date = date.today()
        plt.savefig(f'Capacitance_{num_measurements}_measurements_{date}')
    # Pause for a moment
    time.sleep(1)   # Adjust sleep time as needed 
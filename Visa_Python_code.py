import pyvisa
import numpy as np
import pandas as pd
import time
#print(np.array([1,2,3,4]))
rm = pyvisa.ResourceManager() #make the 'resource manager' object through VISA
print(rm.list_resources())#shows what connections are available 

'''then, once a printed instruments such as 'GPIB0::14::INSTR' is returned, find your instrument name and call label it, i.e. for AH 2550 Bridge:
AH_2550 = rm.open_resource('GPIB0::14::INSTR')
Then make it identify itself to confirm.
print(AH_2550.query('*IDN?'))
which is equivalent to the following 2 lines 
AH_2550.write('*IDN?')
print(AH_2550.read())
values = AH_2550.query_ascii_values('CONT?', container=numpy.array, separator='$')
'''
AH_2550 = rm.open_resource('GPIB0::28::INSTR')
print(AH_2550.query('*IDN?'))
#values = AH_2550.query_ascii_values('SINGLE', container=np.array)
#print(f"values are {values}")

def continuous(no_of_measurements, interval_in_seconds=1):

    '''takes a certain number of single measurements of capacitance and loss with a set interval between each measurement
      and puts them into a csv file along with a timestamp'''
    
    header = ['Capacitance(pF)', 'Loss (nSiemens)']
    df =pd.DataFrame(columns=header) #df of nos to put into csv file at the end
    
    for i in range(no_of_measurements):
        data_trans = []
        AH_2550.write('single')
        time.sleep(0.1)#waits as the AH is slow at times to do measurements 
        raw_data = AH_2550.read_raw()
        split_data = raw_data.split()#splits data at every whitespace, can then index through each split string
        data_trans = [float(split_data[1]), float(split_data[3])]
        print(data_trans)
        df.loc[i] = data_trans
        time.sleep(interval_in_seconds)
    df.to_csv('test.csv', index=False)
    return ('finished')



continuous(10,1)





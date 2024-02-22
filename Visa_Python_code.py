import pyvisa
import numpy as np
import pandas as pd
import time
#print(np.array([1,2,3,4]))
print(time.strftime('%H:%M:%S'))

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
#print(AH_2550.query('*IDN?'))


#values = AH_2550.query_ascii_values('SINGLE', container=np.array)
#print(f"values are {values}")

def continuous(no_of_measurements, filename, interval_in_seconds=0.5):

    '''takes a certain number of single measurements of capacitance and loss with a set interval (default 1 second) between each measurement
      and puts them into a csv file titled "filename" along with a timestamp'''
    
    header = ['Capacitance(pF)', 'Loss (nSiemens)', 'Timestamp (24hr)']
    df =pd.DataFrame(columns=header) #df of nos to put into csv file at the end
    
    for i in range(no_of_measurements):
        data_trans = []
        AH_2550.write('single')
        time.sleep(0.1)#waits as the AH is slow at times to do measurements 
        raw_data = AH_2550.read_raw()
        split_data = raw_data.split()#splits data at every whitespace, can then index through each split string
        timestamp = time.strftime('%H:%M:%S')
        try:
            data_trans = [float(split_data[1]), float(split_data[3]), timestamp]#select string's that are cap and loss and make them floats
        except:
            data_trans = ['NaN', 'NaN', timestamp]#if data cannot be converted to float this can happens when a value isnt produced by the AH2550 and instead 'PF' and 'NS'
                                                  #are then the 1st and 3rd index, this is useless data and the sleep time after writing may need changing
        print(data_trans)
        df.loc[i] = data_trans
        time.sleep(interval_in_seconds)
    df.to_csv(filename+'.csv', index=False)
    return ('finished')


continuous(1800,'Cu_py_5k_max_strain_test_200to_neg_200V')


 




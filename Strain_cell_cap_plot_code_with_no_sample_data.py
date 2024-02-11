import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#capacitance data and delta V data 


#Ti calibration capacitance and temperature

temperature = np.array([300,300,300,200,200,200,100,100,100,100,100,100,100,10,10,10,10,10,10,10,10,10,5,5,5,5,5,5,5,5,5,5])

voltage = np.array([[0,0],[120,120],[0,0],[0,0],[120,-20],[120,-20],[120,-20],[120,120],[0,0],[120,-120],[-120,-120],[-120,120],[0,0],[0,0],[120,120],[0,0],
[120,-120],[-120,-120],[-120,120],[-180,180],[120,120],[0,0],[0,0],[200,-200],[0,0],[-200,200],[0,0],[200,-200],[0,0],[-200,200],[0,0],[0,0]])

#time to find delta voltage using a short loop
del_v = []
for i in range(len(voltage)):
    diff = voltage[i,0]-voltage[i,1]
    del_v.append(diff)
 
#print(del_v)

capacitance = np.array([1.20288,1.20245,1.20344,1.15060,1.02987,1.02387,0.99592,1.09530,1.09739,0.95097,1.09339,1.30729,1.15030, 1.13606,1.13506,
1.13574,1.09280,1.13622,1.18266,1.21346,1.13827,1.12758,1.13752,1.06810,1.132326,1.21492,1.140196,1.067412,1.132460,1.215955,
1.141211,1.140627])

temp_five_k= temperature[-10:]
del_v_five_k = del_v[-10:]
cap_five_k = capacitance[-10:]
five_index_max = np.argmax(cap_five_k)
five_index_min = np.argmin(cap_five_k)

#max V applied at 5K
plt.scatter((temp_five_k[five_index_max], temp_five_k[five_index_min]), (cap_five_k[five_index_max], cap_five_k[five_index_min]), s=30, marker="x", c= 'r')
plt.plot((temp_five_k[five_index_max], temp_five_k[five_index_min]), (cap_five_k[five_index_max], cap_five_k[five_index_min]), c='r', label = '200V, -200V')


#max V applied at 100K
plt.scatter((temperature[9],temperature[11]), (capacitance[9],capacitance[11]), s=30, marker ='x', c = 'b' )
plt.plot((temperature[9],temperature[11]), (capacitance[9],capacitance[11]), label = '120V, -120V', c='b')

#max V applied at 10K
plt.scatter((temperature[16],temperature[18]), (capacitance[16],capacitance[18]), s=30, marker ='x', c = 'orange' )
plt.plot((temperature[16],temperature[18]), (capacitance[16],capacitance[18]), label = '120V, -120V', c='orange')
#constants to work out displacements from capactiance
def displacement(cap):
    alpha= 54.26
    d_0 = 49.44
    c_p = 0.0553
    disp = alpha/(cap-c_p) - d_0
    return(disp)


'''plot_from_300=True
if plot_from_300 ==True:
  plt.scatter(temp[3:], Ti_cal_cap[3:], s=30, marker="x")
else:
  plt.scatter(temp, Ti_cal_cap, s=30, marker="x")'''

#plt.scatter(temp_five_k, cap_five_k, s=30, marker="x")

plt.xlabel('Temperature(K)')
#plt.xlabel('Delta Voltage (V)')

plt.ylabel('Capacitance (pF)')
plt.legend()
plt.grid()
plt.show()






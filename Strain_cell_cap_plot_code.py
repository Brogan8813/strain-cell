# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
#capacitance data and delta V data 
cap = np.array([1.2029, 1.2010, 1.2017, 1.0953, 1.0722, 1.3665, 1.3464])
delta_v = np.array([0,0,0,120,140,-140,-120])

#Ti calibration capacitance and temperature
Ti_cal_cap = np.array([1.2057, 1.2698, 1.25429, 1.20386, 1.18567, 1.18550, 1.155240, 1.15442, 1.15413, 1.13536, 
                       1.133878, 1.13372,  1.11322, 1.10644, 1.103169, 1.10361, 1.10615, 1.10637, 1.10639, 1.110238, 1.113029, 
                         1.113050, 1.117552, 1.121477, 1.121462, 1.133911,  1.134057, 1.134065])
temp = np.array([300, 340, 340, 300, 300, 300, 250, 250, 250, 200, 200, 200, 100, 50, 10, 10, 50, 50, 50, 100, 100, 100, 150, 150, 150, 200, 200, 200])
#constants to work out displacements from capactiance
alpha= 54.26
d_0 = 49.44
c_p = 0.0553
plot_from_300=True


disp = alpha/(cap-c_p) - d_0
#plt.scatter(delta_v, cap)
if plot_from_300 ==True:
  plt.scatter(temp[3:], Ti_cal_cap[3:], s=30, marker="x")
else:
  plt.scatter(temp, Ti_cal_cap, s=30, marker="x")
#plt.plot(temp, Ti_cal_cap)
plt.xlabel('Temperature(K)')
#plt.xlabel('Delta Voltage (V)')

plt.ylabel('Capacitance (pF)')
plt.grid()
plt.show()



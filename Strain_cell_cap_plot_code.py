# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
#capacitance data and delta V data 
cap = np.array([1.2029, 1.2010, 1.2017, 1.0953, 1.0722, 1.3665, 1.3464])
delta_v = np.array([0,0,0,120,140,-140,-120])

#constants to work out displacements from capactiance
alpha= 54.26
d_0 = 49.44
c_p = 0.0553

disp = alpha/(cap-c_p) - d_0
plt.scatter(delta_v, cap)
#plt.xlabel('Displacement (um)')
plt.xlabel('Delta Voltage (V)')
plt.ylabel('Capacitance (pF)')
plt.grid()
plt.show()

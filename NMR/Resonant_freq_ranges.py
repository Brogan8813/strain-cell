
import numpy as np

#Code to show range of possible resonance frequencies for given conditions in NMR circuit for series parallel and parallel series setups


#Series Parallel:

#Coax cable impedance in Ohms
coax_imp = 50 

#max and min capacitances in pF
C_match_1 = np.array([1, 120]) 
C_match_2 = np.array([1, 120]) 
C_tune = np.array([1, 120])

#convert to F
C_match_tot = C_match_1*10**-12 +C_match_2*10**-12
C_tune = C_tune*10**-12

#quality factor of coil Q
Q = 210 

#Inductance of coil
coil_turns = 20
medium_permeability =  np.pi*4*10**-7 #vacuum value
coil_length = 3 #units in cm, side on measured
coil_diameter = 1 #units in cm from top down
wire_thickness = 200*10**-4 #units of cm

coil_area = (np.pi)*coil_diameter**2/4 
coil_L = (coil_turns**2 * (coil_diameter/2)**2)/(9*coil_diameter/2 + 10*coil_length) *1/2.54 *1/1.00000037 *10**-6 #in henrys
#the 1/2.54 is a unit correction from inches to cm, the 1.00000037 is correction to vacuum from air (rel permeability) the 10^-6 is to convert from micro H to H
print(coil_L)


#pick your circuit type by making it True and the other False
Series_parallel = False
Parallel_series = True

if Series_parallel and not Parallel_series:
    res_f = (1/(2*np.pi) * 1/np.sqrt(coil_L*(C_match_tot+C_tune)))*10**-6 #resonant freq in MHz
    print(f'Series Parallel resonant frequency range is: {res_f}MHz')

if not Series_parallel and Parallel_series:
    C_tot = 1/(C_match_tot**-1 +C_tune**-1)
    res_f = (1/(2*np.pi) * 1/np.sqrt(coil_L*C_tot))*10**-6 #resonant freq in MHz
    print(f'Parallel Series resonant frequency range is: {res_f}MHz')

elif Series_parallel and Parallel_series:
    print('Check the true false statements, one must be true, one must be false to show which circuit you are using')
elif not Series_parallel and not Parallel_series:
    print('Check the true false statements, one must be true, one must be false to show which circuit you are using')


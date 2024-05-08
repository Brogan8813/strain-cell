
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

#Inductance of coil the below are defaults
'''
coil_turns = 20
coil_length = 3 #units in cm, side on measured
coil_diameter = 1 #units in cm from top down
wire_thickness = 200*10**-4 #units of cm
'''


'''Change the below values for your coil'''
coil_turns = 5
coil_length = 0.8 #units in cm, side on measured
coil_diameter = 0.7 #units in cm from top down
wire_thickness = 0.69*10**-3 #units of cm

medium_permeability =  np.pi*4*10**-7 #vacuum value

coil_area = (np.pi)*(coil_diameter**2)/4
#calculate coil_L via 2 methods. Method 1, may be  better for tightly spaced coils : 
coil_L = (coil_turns**2 * (coil_diameter/2)**2)/(9*coil_diameter/2 + 10*coil_length) *1/2.54 *1/1.00000037 *10**-6 #in henrys
#the 1/2.54 is a unit correction from inches to cm, the 1.00000037 is correction to vacuum from air (rel permeability) the 10^-6 is to convert from micro H to H

#coil inductance method 2, may be better for widely spaced coils?:
coil_L_2 = coil_turns**2/(coil_length/(medium_permeability*1/1.00000037*coil_area))

print(f'coil inductance is: {coil_L} or {coil_L_2} H')

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


'''Impedance matching section, once you know the range of your resonance condition you need to calculate the impedance matching conditions'''
'''NB. THIS ONLY WORKS FOR PARALLEL SERIES CIRCUITS CURRENTLY, CHECK NUTS AND BOLTS NMR FOR SERIES PARALLEL CONDITION'''

impedance_to_match = 50 #ohms, the impedance you want the circuit to be matched, to prevent reflection this is the source impedance (usually 50 ohms from the preamp)
internal_r_coil = 0.1 #ohms, the resistance of the coil wire
ang_frequency = np.pi*2*210*10**6 #the angular frequency you want resonance at
inductance = coil_L #inductance of the coil calculated before, in henrys 

#this code produces the matching condition in the form of the ratio of C/(C+C') but when tuning using this remember that C'>>C is the ideal condition

capacitance_ratio = (impedance_to_match*internal_r_coil)**0.5/(ang_frequency*inductance)

#can this be achieved with the capacitor values given earlier?
C_match_min = np.min(C_match_tot)
C_match_max = np.max(C_match_tot)
C_tune_min = np.min(C_tune)
C_tune_max = np.max(C_tune)

cap_ratio_min = C_tune_min/(C_tune_min+C_match_max)
cap_ratio_max = C_tune_max/(C_tune_max+C_match_min)

if capacitance_ratio<cap_ratio_min:
    print('true')
    text = 'therefore this matching cannot be completed, use a bigger matching capacitor or a smaller coil inductance'
if capacitance_ratio>cap_ratio_max:
    text = 'something has gone really wrong, this should never happen!'
elif capacitance_ratio<cap_ratio_max and capacitance_ratio>cap_ratio_min:
    text = 'this ratio can be achieved within the current capacitor setup'


print(f'Capacitance ratio: C/(C+C\') ={capacitance_ratio}, max and min possible ratios with these capacitors:{cap_ratio_max},{cap_ratio_min}, {text}')



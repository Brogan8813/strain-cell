import numpy as np

#Code to show range of possible resonance frequencies for given conditions in NMR circuit for series parallel and parallel series setups


#Series Parallel:

#Coax cable impedance in Ohms
coax_imp = 50 

#capacitances in pF
C_match = 10 
C_tune = 5

#quality factor of coil Q
Q = 190 

#angualr frequencies to test(?) at
ang_freq = np.arange(0, 1000, 50)




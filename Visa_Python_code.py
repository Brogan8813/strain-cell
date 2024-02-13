import pyvisa
import numpy as np
print(np.array([1,2,3,4]))
rm = pyvisa.ResourceManager()
print(rm.list_resources())
#pyvisa.ResourceManager('@py')
'''then, once a printed instruments such as 'GPIB0::14::INSTR' is returned, find your instrument name and call label it, i.e. for AH 2550 Bridge:
AH_2550 = rm.open_resource('GPIB0::14::INSTR')
Then make it identify itself to confirm.
print(AH_2550.query('*IDN?'))
which is equivalent to the following 2 lines 
AH_2550.write('*IDN?')
print(AH_2550.read())
values = AH_2550.query_ascii_values('CONT?', container=numpy.array, separator='$')
'''
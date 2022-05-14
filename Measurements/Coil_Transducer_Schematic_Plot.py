# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:31:44 2022

@author: thierry.schwaller
"""
import matplotlib.pyplot as plt
from FrequencyResponse import ImpedanceCSV
from Impedance import Impedance
import pandas as pd
import numpy as np

path_angle = "../Messungen_FB_TS_BA/02_Meas/Ang_Z"
path_magnitude = "../Messungen_FB_TS_BA/02_Meas/Mag_Z"

impedanceCSV_transducer = ImpedanceCSV(path_magnitude, path_angle)
impedanceCSV_transducer.setup_folders()
impedanceCSV_transducer.loadValues()

imps = []
for i in range(10):
    imp = Impedance((impedanceCSV_transducer.magnitudes[i])[" Formatted Data"]
                    ,(impedanceCSV_transducer.angle[i])[" Formatted Data"]
                    ,(impedanceCSV_transducer.angle[i])["Frequency"])
    imps.append(imp)

print(len(imps))
# coil_mag = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_220u_25kHz_50kHz/MAG_Z_001.CSV")
# coil_ang = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_220u_25kHz_50kHz/ANG_Z_001.CSV")

# imp_coil = Impedance(coil_mag[" Formatted Data"]
#                               , coil_ang[" Formatted Data"]
#                               , coil_mag["Frequency"])

# coil_mag = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_220u_25kHz_50kHz/MAG_Z_001.CSV")
# coil_ang = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_220u_25kHz_50kHz/ANG_Z_001.CSV")

# imp_coil_2 = Impedance(coil_mag[" Formatted Data"]
#                               , coil_ang[" Formatted Data"]
#                               , coil_mag["Frequency"])

# Calculate schematic
imp = imps[0] | imps[1] | imps[2]  | imps[3]  | imps[4]  | imps[5]  | imps[6] | imps[7]  
imp_tot = imp 

# Plot Coil
c = pd.read_csv("Messungen_22kHz_55kHz_100Hz.csv")
f = np.arange(22,55.1,0.1)
for i,p in enumerate(c["Mag_dB"]):
    print(f"({f[i]} ,{p})")

mag =np.real(imp.magnitude*np.exp(complex(0,1)*imp.angle/180*np.pi))

# Plot 
fig,ax = plt.subplots()
ax_p = ax.twinx()
#ax.plot(imp_tot.frequency,imp_tot.magnitude,"orange",label = "With Coil")
ax.plot(imp.frequency,np.real(imp.magnitude*np.exp(complex(0,1)*imp.angle/180*np.pi)),"blue",label = "Transducers")
ax.plot(f*1000,c["Mag_dB"])
ax.set_xlim((25000,55000))
# ax_p.plot(imp_tot.frequency,imp_tot.angle,"orange",linestyle="-.")
# ax_p.plot(imp.frequency,imp.angle,"blue",linestyle="-.")
ax.legend(loc='upper left')
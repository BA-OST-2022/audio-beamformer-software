# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:38:46 2022

@author: thierry.schwaller
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import fnmatch
from FrequencyResponse import ImpedanceCSV

class Impedance():
    def __init__(self,magnitude,angle, frequency):
        self.magnitude = magnitude
        self.angle = angle
        self.frequency = frequency
        self.impedance = magnitude * np.exp(complex(0,1)*(angle/180*np.pi))
    
    def __add__(self, other):
        totImpedance = self.impedance + other.impedance
        return Impedance(np.abs(totImpedance),np.angle(totImpedance,deg=True))
    
    def __or__(self, other):
        totImpedance = (self.impedance * other.impedance)/(self.impedance + other.impedance)
        return Impedance(np.abs(totImpedance),np.angle(totImpedance,deg=True),self.frequency)
    

path_angle = "Messungen_FB_TS_BA/02_Meas/Ang_Z"
path_magnitude = "Messungen_FB_TS_BA/02_Meas/Mag_Z"

impedanceCSV_transducer = ImpedanceCSV(path_magnitude, path_angle)
impedanceCSV_transducer.loadValues()

coil_mag = pd.read_csv("Messungen_FB_TS_BA/03_Coils/680u/MAG_Z_001.CSV")
coil_ang = pd.read_csv("Messungen_FB_TS_BA/03_Coils/680u/MAG_Z_001.CSV")
imp_coil = Impedance(coil_mag[" Formatted Data"]
                              , coil_mag[" Formatted Data"]
                              , coil_mag["Frequency"])

imps = []
for i in range(20):
    imp = Impedance((impedanceCSV_transducer.magnitudes[i])[" Formatted Data"]
                    ,(impedanceCSV_transducer.angle[i])[" Formatted Data"]
                    ,(impedanceCSV_transducer.angle[i])["Frequency"])
    imps.append(imp)

imp = imps[8] | imps[9] | imps[10] | imps[11] | imps[12] | imps[13] | imps[14] | imps[15]

fig, ax = plt.subplots()
ax.plot(imp_coil.frequency,imp_coil.magnitude)
fig,ax = plt.subplots()
ax_p = ax.twinx()
ax.plot(imp.frequency,imp.magnitude)
ax_p.plot(imp.frequency,imp.angle,"g",)
ax.plot(imps[0].frequency,imps[0].magnitude)
ax.set_ylim((0,1000))
ax_p.plot(imps[0].frequency,imps[0].angle,"g--")
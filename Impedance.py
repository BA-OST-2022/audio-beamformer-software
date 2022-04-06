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
        self.impedance = magnitude * np.exp(complex(0,1)*angle)
    
    def __add__(self, other):
        totImpedance = self.impedance + other.impedance
        return Impedance(np.abs(totImpedance),np.angle(totImpedance))
    
    def __or__(self, other):
        totImpedance = (self.impedance * other.impedance)/(self.impedance + other.impedance)
        return Impedance(np.abs(totImpedance),np.angle(totImpedance),self.frequency)
    

path_angle = "Messungen_FB_TS_BA/02_Meas/Ang_Z"
path_magnitude = "Messungen_FB_TS_BA/02_Meas/Mag_Z"

impedanceCSV = ImpedanceCSV(path_magnitude, path_angle)
impedanceCSV.loadValues()

imp = Impedance((impedanceCSV.magnitudes[0])[" Formatted Data"]
                ,(impedanceCSV.angle[0])[" Formatted Data"]
                ,(impedanceCSV.angle[0])["Frequency"])

fig,ax = plt.subplots()
imp = imp | imp | imp | imp | imp | imp | imp | imp | imp
ax.plot(imp.frequency,imp.magnitude)
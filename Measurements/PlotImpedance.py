# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:33:19 2022

@author: thierry.schwaller
"""

import matplotlib.pyplot as plt
from FrequencyResponse import ImpedanceCSV
from Impedance import Impedance
import pandas as pd


coil_mag = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_680u_1kHz_20MHz/MAG_Z_001.CSV")
coil_ang = pd.read_csv("Messungen_FB_TS_BA/001_MEAS/Coil_680u_1kHz_20MHz/ANG_Z_001.CSV")

imp_coil = Impedance(coil_mag[" Formatted Data"]
                              , coil_ang[" Formatted Data"]
                              , coil_mag["Frequency"])


fig, ax = plt.subplots()
fig.suptitle(f"150uH Coil", fontsize=16)
ax_p = ax.twinx()
ax.loglog(imp_coil.frequency,imp_coil.magnitude)
ax_p.plot(imp_coil.frequency,imp_coil.angle,"g--")
ax.set_xlim((0,20000000))
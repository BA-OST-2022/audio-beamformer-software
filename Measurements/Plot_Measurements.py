# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 12:09:13 2022

@author: thierry.schwaller
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


c = pd.read_csv("Messungen_22kHz_55kHz_100Hz.csv")
f = np.arange(22,55.1,0.1)
for i,p in enumerate(c["Mag_dB"]):
    print(f"({f[i]} ,{p})")



fig, ax = plt.subplots()
lin_y = 10**(c["Mag_dB"]/20)
lin_y = lin_y / max(lin_y)
ax.plot(f,lin_y)
f = np.arange(40.2,55,0.1)
t = 1/(f-40)**(4/5)
t = t/max(t)
ax.plot(f, t)

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:19:44 2022

@author: thierry.schwaller
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import fnmatch
class ImpedanceCSV:
    def __init__(self,path_magnitude,path_angle):
        self.path_magnitude = path_magnitude
        self.path_angle = path_angle
        self.newpath_angle = f"{self.path_angle}/SetupFolder"  
        self.newpath_mag =  f"{self.path_magnitude}/SetupFolder/Mag_Z_"
        self.nr_of_files = len(fnmatch.filter(os.listdir(f'{self.path_magnitude}'), '*.CSV*'))
        self.magnitudes =  []
        self.angle =  []
        
    def setup_folders(self):
        if not os.path.exists(self.newpath_angle):
            os.makedirs(self.newpath_angle)
        if not os.path.exists(self.newpath_mag):
            os.makedirs(self.newpath_mag)
        
        for i in range(1,self.nr_of_files + 1):
            with open(f"{self.path_angle}/Ang_Z_{i:03}.CSV") as f:
                path_new = f"{self.newpath_angle}/Ang_Z_{i:03}_U.CSV"
                with open(path_new,"w+") as p:
                    for line in f.readlines():
                        if (line[1] == "#"):
                            continue
                        p.writelines(line)
            with open(f"{self.path_magnitude}/Mag_Z_{i:03}.CSV") as f:
                path_new = f"{self.newpath_mag}/Mag_Z_{i:03}_U.CSV"
                with open(path_new,"w+") as p:
                    for line in f.readlines():
                        if (line[1] == "#"):
                            continue
                        p.writelines(line)
    def loadValues(self):
        for file in range(1,self.nr_of_files+1):
            self.magnitudes.append(pd.read_csv(f"{self.newpath_mag}/Mag_Z_{file:03}_U.CSV")) 
            self.angle.append(pd.read_csv(f"{self.newpath_angle}/Ang_Z_{file:03}_U.CSV"))
            
    def plot_single(self,start_f,stop_f):
        for i in range(1,self.nr_of_files + 1):
            angle = self.angle[i-1]
            magnitude = self.magnitudes[i-1]
            fig, ax = plt.subplots()
            ax_m = ax.twinx()
            ax.plot(magnitude["Frequency"]
                    ,magnitude[" Formatted Data"]
                    , "b")
            ax_m.plot(angle["Frequency"]
                    ,angle[" Formatted Data"]
                    , "r--")
            ax.set_ylim((0,8000))
            ax.set_xlim((start_f,stop_f))
            
    def plot_all(self,start_f,stop_f):
        fig, ax = plt.subplots()
        ax_m = ax.twinx()
        for i in range(1,self.nr_of_files + 1):
            angle = self.angle[i-1]
            magnitude = self.magnitudes[i-1]
            ax.plot(magnitude["Frequency"]
                    ,magnitude[" Formatted Data"]
                    , "b"
                    , alpha=0.2)
            ax_m.plot(angle["Frequency"]
                    ,angle[" Formatted Data"]
                    , "r--"
                    , alpha=0.2)
            ax.set_ylim((0,8000))
            ax.set_xlim((start_f,stop_f))

path_angle = "Messungen_FB_TS_BA/02_Meas/Ang_Z"
path_magnitude = "Messungen_FB_TS_BA/02_Meas/Mag_Z"



impedanceCSV = ImpedanceCSV(path_magnitude, path_angle)
#impedanceCSV.setup_folders()
impedanceCSV.loadValues()
#impedanceCSV.plot_single(25000, 50000)
#impedanceCSV.plot_all(25000, 50000)
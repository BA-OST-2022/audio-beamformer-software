# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:38:46 2022

@author: thierry.schwaller
"""
import numpy as np

class Impedance():
    def __init__(self,magnitude,angle, frequency):
        self.magnitude = magnitude
        self.angle = angle
        self.frequency = frequency
        self.impedance = magnitude * np.exp(complex(0,1)*(angle/180*np.pi))
    
    def __add__(self, other):
        totImpedance = self.impedance + other.impedance
        return Impedance(np.abs(totImpedance),np.angle(totImpedance,deg=True),self.frequency)
    
    def __or__(self, other):
        totImpedance = (self.impedance * other.impedance)/(self.impedance + other.impedance)
        return Impedance(np.abs(totImpedance),np.angle(totImpedance,deg=True),self.frequency)
    
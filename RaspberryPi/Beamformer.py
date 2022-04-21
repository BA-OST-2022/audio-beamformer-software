#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:13:15 2022

@author: root
"""
from SPI_Interface import SPIInterface
import numpy as np
import time

class Beamformer():
    def __init__(self,
                 spi_interface,
                 temperature=22,
                 row_count=6,
                 distance=14.75e-3):
        self.spi_interface = spi_interface
        self.temperature = temperature
        self.speed_of_sound = 331.5 + 0.607*temperature
        self.row_count = row_count
        self.distance = distance
        self.window_types = {"rect": self.rectWindow(),
                             "cosine": self.cosineWindow(),
                             "hann": self.hannWindow(),
                             "hamming": self.hammingWindow(),
                             "blackman": self.blackmanWindow(),
                             "cheby": self.chebyWindow()}

    def rectWindow(self):
        gains = [1] * self.row_count
        return gains

    def cosineWindow(self):
        gains = np.sin(np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def hannWindow(self):
        gains = np.sin(np.arange(self.row_count)*np.pi/(self.row_count-1))**2
        gains /= max(gains)
        return gains

    def hammingWindow(self):
        gains = 0.54 - 0.46 * np.cos(2*np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def blackmanWindow(self):
        gains = 0.42 - 0.5 * np.cos(2*np.arange(self.row_count)*np.pi/(self.row_count-1)) + 0.08 * np.cos(4*np.arange(self.row_count)*np.pi/(self.row_count-1))
        gains /= max(gains)
        return gains

    def chebyWindow(self):
        alpha = 5
        beta = np.cosh(1/self.row_count*np.arccosh(10**alpha))
        freq_dom = np.array([self.chebyPol(beta*np.cos(np.pi * val /(self.row_count+1)))/self.chebyPol(beta) for val in np.arange(self.row_count)])
        gains = np.real(np.fft.fftshift(np.fft.ifft(freq_dom)))
        gains /= max(gains)
        return gains

    def chebyPol(self, val):
        N = self.row_count
        if val <= -1:
            return (-1)**N*np.cosh(N*np.arccosh(-val))
        elif val >= 1:
            return np.cosh(N*np.arccosh(val))
        else:
            return np.cos(N*np.arccos(val))

    def steerAngle(self, angle):
        delay = np.arange(self.row_count) * self.distance / self.speed_of_sound * np.sin(angle/180*np.pi)
        if (np.sin(angle/180*np.pi) < 0):
            delay = delay[::-1] * -1
        self.spi_interface.delay = delay
        self.spi_interface.updateSPI()

    def steerAngleBetween(self, min_angle, max_angle, steps, hold_time, loop = 1):
        for i in range(loop):
            for angle in np.linspace(min_angle, max_angle, steps):
                self.steerAngle(angle)
                time.sleep(hold_time)

    def beamFocusing(self, focal_length):
        delay = np.arange(self.row_count) * (self.row_count - np.arange(self.row_count)) * self.distance**2 / (focal_length * 2 *self.speed_of_sound)
        print(delay)

    def setWindow(self, window_type):
        gain = self.window_types[window_type]
        print(gain)
        self.spi_interface.gains = gain
        self.spi_interface.updateSPI()

spi = SPIInterface(channel_count=7, channel_per_fpga=10)
b = Beamformer(spi,row_count=7)
# b.steerAngleBetween(-45, 45, 10, 0.5, 3)
# b.beamFocusing(0.15)
b.setWindow("cheby")
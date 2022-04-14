#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:13:15 2022

@author: root
"""
from SPI_Interface import SPIInterface
import numpy as np

class Beamformer():
    def __init__(self,
                 spi_interface,
                 temperature = 22,
                 row_count = 6,
                 distance = 14.75e-3):
        self.spi_interface = spi_interface
        self.temperature = temperature 
        self.speed_of_sound = 331.5 + 0.607*temperature
        self.row_count = row_count
        self.distance = distance
    def steerAngle(self, angle):
        delay = np.arange(self.row_count) * self.distance / self.speed_of_sound * np.sin(angle/180*np.pi)
        if (np.sin(angle/180*np.pi) < 0):
            delay = delay[::-1] * -1
        self.spi_interface.delay = delay
        print(delay)
        self.spi_interface.updateSPI()


spi = SPIInterface(channel_count=6, channel_per_fpga=10)
b = Beamformer(spi)

b.steerAngle(-45)

        
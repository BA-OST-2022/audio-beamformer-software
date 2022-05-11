#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:45:38 2022

@author: root
"""
import spidev
import numpy as np

class SPIInterface():
    def __init__(self,
                 channel_count,
                 channel_per_fpga,
                 interpolation = 64,
                 modulation_type="DSB",
                 sigma_delta_coeff=2**13):

       self.spi = spidev.SpiDev(0, 0)
       self.spi.max_speed_hz = 1000000
       
       self.channel_per_fpga = channel_per_fpga
       self.channel_count= channel_count
       self.fpga_count = int(np.ceil(channel_count / channel_per_fpga))
       self.gain = np.ones(self.channel_count)
       self.delay = np.ones(self.channel_count) * 0
       # Interpolation value of: 1, 2, 4, ..., 32, 64
       self.interpolation = interpolation
       # Modulation type value: "DSB" / "MAM"
       self.modulation_type = modulation_type
       # Sigma_delta_coeff value: 2^0 ... 2^15  
       self.sigma_delta_coeff = sigma_delta_coeff
       self.sigma_delta_freq = 6.25e6
       self.enable_channel = [True] *  self.channel_count
       
    def updateSPI(self):
        modulation_types = {"MAM": 0, "DSB": 1}
        tick_length = 2 / self.sigma_delta_freq
        
        if not (self.interpolation in [1, 2, 4, 8, 16, 32, 64]):
            raise Exception("Interpolation out of bound")
        if not (self.modulation_type in modulation_types):
            raise Exception("Modulation type not avaiable")
        if not (1 <= self.sigma_delta_coeff <= 32767):
            raise Exception("Sigma delta coeff must be between 1 and 32767")
        if not (any([-1 <= g <= 1 for g in self.gain])):
            raise Exception("Gain between -1 and 1")
        if not (any([0 <= d <= tick_length * 2046 for d in self.delay])):
            raise Exception(f"Delay between 0 and {tick_length * 2046} s")
        
        # Bit [7:4] free 
        settings = 0x00
        settings |= (int(7 - np.log2(self.interpolation)) & 0x03)
        settings |= (int(modulation_types[self.modulation_type]) & 0x01) << 3
        
        sigma_delta = np.array([i for i in (self.sigma_delta_coeff).to_bytes(2, "big")])
        enable = sum([2**i*int(value) for i,value in enumerate(self.enable_channel)]).to_bytes(2, "big")
        
        gain_int = (self.gain * 32767).astype(int)
        gains = np.array([i for gain in gain_int for i in int(gain).to_bytes(2, "big", signed=True)])
        delay_count = (self.delay / tick_length).astype(int)
        delay_count = np.array([i for d in delay_count for i in int(d).to_bytes(2, "big", signed=True)])
        
        spi_data = []
        for fpga in range(self.fpga_count):
            spi_data.append(settings)
            spi_data.append(int(sigma_delta[0]))
            spi_data.append(int(sigma_delta[1]))
            spi_data.append(int(enable[0]))
            spi_data.append(int(enable[1]))
            for channel in range(self.channel_per_fpga):
                if((channel + 1) * (fpga + 1) > self.channel_count):
                    break
                spi_data.append(int(delay_count[channel * 2]))
                spi_data.append(int(delay_count[channel * 2 + 1]))
                spi_data.append(int(gains[channel * 2 + 0]))
                spi_data.append(int(gains[channel * 2 + 1]))

        self.spi.writebytes(spi_data[::-1])
        print(spi_data)
if __name__ == '__main__':   
    s = SPIInterface(channel_count=6, channel_per_fpga=10)
    s.enable_channel = [False] * 6
    s.enable_channel[3] = True
    s.updateSPI()
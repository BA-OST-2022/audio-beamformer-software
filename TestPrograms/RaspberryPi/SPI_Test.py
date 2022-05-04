#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:27:33 2022

@author: root
"""

import spidev

spi_ch = 0
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

spi.writebytes([0xFF])
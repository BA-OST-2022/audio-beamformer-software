#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 11:11:00 2022

@author: pi
"""

import pydbus

bus = pydbus.SystemBus()

adapter = bus.get('org.bluez', '/org/bluez/hci0')
mngr = bus.get('org.bluez', '/')

def list_connected_devices():
    mngd_objs = mngr.GetManagedObjects()
    for path in mngd_objs:
        con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', False)
        if con_state:
            addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
            name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
            print(f'Device {name} [{addr}] is connected')

if __name__ == '__main__':
    list_connected_devices()
    
    # Device Florians iPhone [40:9C:28:5C:A6:90] is connected
    # Device iPhone von Thierry [A8:81:7E:D2:BE:E9] is connected


from vl53l5cx.vl53l5cx import VL53L5CX
from vl53l5cx.api import *

import time
import cv2
import numpy as np

SCALEUP = 50
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 0.4
FONT_COLOR = (0,0,0)
FONT_THICKNESS = 1


driver = VL53L5CX(bus_id=0)
alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")

print("Initialising...")
driver.init()
print("Done!")


_resolution = 8         # 4 or 8
_distanceData = np.zeros((_resolution, _resolution))


# driver.set_ranging_mode(VL53L5CX_RANGING_MODE_CONTINUOUS)
driver.set_sharpener_percent(0)
driver.set_target_order(VL53L5CX_TARGET_ORDER_STRONGEST)
driver.set_resolution(_resolution**2)
driver.set_ranging_frequency_hz(15)
driver.start_ranging()

previous_time = 0
loop = 0
while loop < 1000:
    if driver.check_data_ready():
        ranging_data = driver.get_ranging_data()
        for i in range(driver.get_resolution()):
            val = 4000
            if(ranging_data.target_status[i] != 255):
                val = ranging_data.distance_mm[i]
            if(val == 0):
                val = 4000  
            _distanceData[i // _resolution, i % _resolution] = val

        
        image = (_distanceData * 0.06375).astype('uint8')
        resized = cv2.resize(image, (_resolution * SCALEUP,_resolution * SCALEUP), interpolation= cv2.INTER_NEAREST)
        for j in range(_resolution):
            for k in range(_resolution):
                cv2.putText(resized,
                            '%d' % _distanceData[k,j],
                            (j*SCALEUP+SCALEUP//4,k*SCALEUP+SCALEUP//2),
                            FONT, FONT_SIZE, FONT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
        
        loop += 1
        cv2.imshow('VL53L5 [ESC to quit]', resized)
        if cv2.waitKey(1) == 27:
            break

        

    time.sleep(0.005)
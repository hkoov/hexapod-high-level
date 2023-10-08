import serial
import math
import time
import asyncio
import xbox_control_inputs
import up_down
import async_functions

i = 0

ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)

angle1 = 0
angle2 = 30
angle3 = 30

async_functions.write_angles(ser0, ser1, angle1, angle2, angle3)

controller_path = xbox_control_inputs.find_controller()

height_range = 0

async def main ():
    while True:
        await asyncio.gather(xbox_control_inputs.controller_inputs(controller_path, height_range), 
                             up_down.up_down_degrees(height_range, 50, 80, 132, angle2, angle3), 
                             async_functions.write_angles(ser0, ser1, angle1, angle2, angle3))

asyncio.run(main())
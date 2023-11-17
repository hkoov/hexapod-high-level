import serial
import math
import time
import asyncio
import xbox_control_inputs
import translations
import write_functions

# Initialising serial connections. Still need to figure out left/right
ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)

# Set starting angles and write them to the motors
angle1 = 0
angle2 = 30
angle3 = 30

write_functions.write_angles(ser0, ser1, angle1, angle2, angle3)

# Find the path to the XBox controller - 
controller_path = xbox_control_inputs.find_controller()

# Initialise the height change parameter (probably need some others for the other translations/rotations, and velocity inputs for walking)
height_change = 0

async def angle_change(height_change, height_range, femur, tibia, angle2, angle3):
    angle2, angle3 = translations.up_down_degrees(height_change, height_range, femur, tibia, angle2, angle3)
    await asyncio.sleep(0.01)

async def modify_height (height_change):
    height_change = xbox_control_inputs.controller_inputs(controller_path)
    #await asyncio.sleep(0.01)
    return height_change
    
async def process():
    height_change = await xbox_control_inputs.controller_inputs(controller_path)
    angle_2, angle_3 = translations.up_down_degrees(height_change, 100, 80, 132, angle2, angle3)
    await write_functions.write_angles_async(ser0, ser1, angle1, angle_2, angle_3)



async def main ():
    while True:
        angle2 = 30
        angle3 = 30
        #height_change = 0
        await asyncio.gather(process())

asyncio.run(main())
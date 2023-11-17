import serial
import math
import time
import asyncio
import xbox_control_inputs
import translations
import write_functions
import robot_geometry


# Initialise serial connections. Still need to figure out left/right
ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)


# Set starting angles and write them to the motors
angle1 = 0
angle2 = 30
angle3 = 30

write_functions.write_angles(ser0, ser1, angle1, angle2, angle3)


# Initialise the height change parameter and height change range
# (probably need some others for the other translations/rotations, and velocity inputs for walking)
height_change = 0
height_range = 100


# Define parameters for the robot geometry
coxa = robot_geometry.coxa
femur = robot_geometry.femur
tibia = robot_geometry.tibia


# Find the path to the XBox controller and use it to initialise a controller object
controller_path = xbox_control_inputs.find_controller()

controller = xbox_control_inputs.controller(controller_path)

while True:
    try:
        controller.update()
    except:
        continue
    height_change = 1 - controller.L_y_axis/65535
    angle2, angle3 = translations.up_down_degrees(height_change, height_range, femur, tibia, angle2, angle3) 
    write_functions.write_angles(ser0, ser1, angle1, angle2, angle3)

"""
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

#asyncio.run(main())

from evdev import InputDevice, categorize, ecodes
dev = InputDevice(controller_path)

for event in dev.read_loop():
#    if event.type == ecodes.EV_KEY:
     print(event)
"""
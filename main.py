import serial
import math
import time
import asyncio
import xbox_control_inputs
import translations
import write_functions
import robot_geometry
import evdev


# Initialise serial connections. Still need to figure out left/right
ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)


# Set starting angles and write them to the motors
angle1_default = 0
angle2_default = 30
angle3_default = 30

#write_functions.write_angles(ser0, ser1, angle1_default, angle2_default, angle3_default)


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


# Enclose the angle calcs and serial write instructions in this async function 
# This gives a continuous stream of events which are then used to change the inputs
# Additional movements need to be coded after the controller.update(event) line
async def helper(dev_path, angle1_default, angle2_default, angle3_default):
    dev = evdev.InputDevice(dev_path)
    async for event in dev.async_read_loop():
        controller.update(event)

        height_change = 1 - controller.L_y_axis/65535
        angle2, angle3 = translations.up_down_degrees(height_change, height_range, femur, tibia, angle2_default, angle3_default) 
        write_functions.write_angles(ser0, ser1, angle1_default, angle2, angle3)

loop = asyncio.get_event_loop()
loop.run_until_complete(helper(controller.path, angle1_default, angle2_default, angle3_default))

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
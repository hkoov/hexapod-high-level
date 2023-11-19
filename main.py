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


# Set the default angles for each motor. Translations and rotations will be applied sequentially to this starting position
angle1_default = 0
angle2_default = 30
angle3_default = 30


# Initialise the height change parameter and height change range
# (probably need some others for the other translations/rotations, and velocity inputs for walking)
z_trans_change = 0
z_trans_range = 100


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
        # Update the controller state based on the event values read
        controller.update(event)

        
        # Define the angles to be their default values to start
        angle1 = angle1_default
        angle2 = angle2_default
        angle3 = angle3_default

        ### THIS IS WHERE THE OTHER TRANSLATIONS AND ROTATIONS WILL NEED TO BE APPLIED

        # Calculate the Z-axis translation and calculate the resulting angles
        z_trans_change = 1 - controller.L_y_axis/65535
        angle2, angle3 = translations.up_down_degrees(z_trans_change, z_trans_range, femur, tibia, angle2, angle3) 
        
        
        # Finally write the angles to the motors
        write_functions.write_angles(ser0, ser1, angle1, angle2, angle3)


# Generate an event loop using the defined async function
loop = asyncio.get_event_loop()

# Run the loop
loop.run_until_complete(helper(controller.path, angle1_default, angle2_default, angle3_default))

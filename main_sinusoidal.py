import serial
import math
import time
import asyncio
import xbox_control_inputs
import translations
import rotations
import write_functions
import robot_geometry
import evdev
import copy

### DEBUG FLAG
debug_flag = False

# Initialise serial connections. Still need to figure out left/right
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)
ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)


# Set the default angles for each motor. Translations and rotations will be applied sequentially to this starting position
l1_angles = [-45, 45, 45]
r1_angles = [45, 45, 45]
l2_angles = [-90, 45, 45]
r2_angles = [90, 45, 45]
l3_angles = [-135, 45, 45]
r3_angles = [135, 45, 45]

angle_defaults = [l1_angles, r1_angles, l2_angles, r2_angles, l3_angles, r3_angles]

write_functions.write_angles(ser0, ser1, angle_defaults, debug=debug_flag)

# Set the joint offsets
l1_offsets = [robot_geometry.x_offsets[1], robot_geometry.y_offsets[0]]
r1_offsets = [robot_geometry.x_offsets[2], robot_geometry.y_offsets[0]]
l2_offsets = [robot_geometry.x_offsets[0], robot_geometry.y_offsets[1]]
r2_offsets = [robot_geometry.x_offsets[3], robot_geometry.y_offsets[1]]
l3_offsets = [robot_geometry.x_offsets[1], robot_geometry.y_offsets[2]]
r3_offsets = [robot_geometry.x_offsets[2], robot_geometry.y_offsets[2]]

joint_offsets = [l1_offsets, r1_offsets, l2_offsets, r2_offsets, l3_offsets, r3_offsets]

# Initialise the height change parameter and height change range
# (probably need some others for the other translations/rotations, and velocity inputs for walking)
y_trans_change = 0
y_trans_range = 30

x_trans_change = 0
x_trans_range = 30

z_trans_change = 0
z_trans_range = 50

roll_change = 0
roll_range = 12     # Specified in degrees

pitch_change = 0
pitch_range = 12     # Specified in degrees

yaw_change = 0
yaw_range = 20     # Specified in degrees

# Define parameters for the robot geometry
coxa = robot_geometry.coxa
femur = robot_geometry.femur
tibia = robot_geometry.tibia

# Initialise a variable to use in the sine loop
j = 0


while True:
    j = j + 1          
    j = j % 360     # Set to zero if it gets to 180

    # Reset the leg positions to their default values
    legs = copy.deepcopy(angle_defaults)

    # Calculate the translations to be applied (all between -1 and 1)
    y_trans_change =    - math.sin(j / 180 * math.pi)
    x_trans_change =    - math.cos(j / 180 * math.pi)
    z_trans_change =    0.5 #+ 0.5 * math.sin(j / 180 * math.pi)

    roll_change =       - math.cos(j / 180 * math.pi)
    pitch_change =      math.sin(j / 180 * math.pi)
    yaw_change =        0 #math.sin(j / 180 * math.pi)

    for i in range(6):
        leg = legs[i]
        legs[i][0], legs[i][1], legs[i][2] = translations.forward_back_degrees(y_trans_change, y_trans_range, coxa, femur, tibia, leg)
        legs[i][0], legs[i][1], legs[i][2] = translations.right_left_degrees(x_trans_change, x_trans_range, coxa, femur, tibia, leg)
        legs[i][0], legs[i][1], legs[i][2] = translations.up_down_degrees(z_trans_change, z_trans_range, coxa, femur, tibia, leg)

        legs[i][0], legs[i][1], legs[i][2] = rotations.roll(roll_change, roll_range, joint_offsets[i][0], joint_offsets[i][1], coxa, femur, tibia, leg)
        legs[i][0], legs[i][1], legs[i][2] = rotations.pitch(pitch_change, pitch_range, joint_offsets[i][0], joint_offsets[i][1], coxa, femur, tibia, leg)
        legs[i][0], legs[i][1], legs[i][2] = rotations.yaw(yaw_change, yaw_range, joint_offsets[i][0], joint_offsets[i][1], coxa, femur, tibia, leg)

    
    # Finally write the angles to the motors
    write_functions.write_angles(ser0, ser1, legs, debug=debug_flag)

    # Sleep to slow it down
    time.sleep(0.003)

    print(j)
    

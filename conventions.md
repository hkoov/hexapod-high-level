ser0 is for the LEFT half of the robot
ser1 is for RIGHT

Motor 1 is at the front, 3 is at the back

Joint 1 articulates the coxa
Joint 2 articulates the femur
Joint 3 articulates the tibia

### Joint angles:
#### Joint 1
0 degrees is out to the side and the angle increases going backwards, so leg 1 has a default of -45 degrees, leg 2 0 degrees, and leg 3 45 degrees

#### Joint 2
0 degrees is straight up, and 180 degrees is straight down

#### Joint 3
The motor position starts at 0 degrees (the downward most position), and moves to 135 degrees (the upward most)
At zero degrees, the motor is at 45 degrees to the femur, but since it is bent, the actual angle from the femur to rhe tip of the tibia is 25 degrees when the motor is set to 0 degrees.



Have a separate module that reads the controller events and writes them to an object

The main loop then reads that object and translates it into the desired movements and joint angles


import serial
import math
import time

i = 0

#ser1 = serial.Serial('/dev/serial0', 115200, timeout=0.050)

while True:
    angle = 0

    if i == 360:
        i = 0

    rads = (i / 360) * 2 * math.pi

    frac = math.sin(rads)

    i += 1

    angle = frac * 45

    angle_str = str(int(angle))

    string1 = angle_str + "," + "0,0," + angle_str + "," + "0,0," + angle_str + "," + "0,0" 

    print(string1)

    # ser1.write(string1)

    time.sleep(1/100)


    
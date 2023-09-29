import serial
import math
import time

i = 0

ser0 = serial.Serial('/dev/ttyACM0', 115200, timeout=0.050)
ser1 = serial.Serial('/dev/ttyACM1', 115200, timeout=0.050)

while True:
    angle1 = 0
    angle2 = 0
    angle3 = 0

    if i == 360:
        i = 0

    rads = (i / 360) * 2 * math.pi

    frac = math.sin(rads)

    i += 1

    angle1 = frac * 45
    angle2 = 30 - frac * 30
    angle3 = 30 + frac * 30

    angle1_str = str(int(angle1))
    angle2_str = str(int(angle2))
    angle3_str = str(int(angle3))

    string1 = angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str

    print(string1)

    ser0.write(str.encode(string1 + "\n"))
    ser1.write(str.encode(string1 + "\n"))

    time.sleep(1/100)


    
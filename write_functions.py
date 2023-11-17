import asyncio

async def write_angles_async(ser0, ser1, angle1, angle2, angle3):
    """
    Takes two serial objects and three integer angles (in degrees), and writes the three degrees to the nine motors controlled by each controller.
    """
    #angle1 = 0
    #angle2 = 0
    #angle3 = 0

    angle1_str = str(int(angle1))
    angle2_str = str(int(angle2))
    angle3_str = str(int(angle3))

    string1 = angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str

    print(string1)

    ser0.write(str.encode(string1 + "\n"))
    ser1.write(str.encode(string1 + "\n"))

    await asyncio.sleep(0.01)


def write_angles(ser0, ser1, angle1, angle2, angle3):
    """
    Takes two serial objects and three integer angles (in degrees), and writes the three degrees to the nine motors controlled by each controller.
    """
    #angle1 = 0
    #angle2 = 0
    #angle3 = 0

    angle1_str = str(int(angle1))
    angle2_str = str(int(angle2))
    angle3_str = str(int(angle3))

    string1 = angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str + "," + angle1_str + "," + angle2_str + "," + angle3_str

    print(string1)

    ser0.write(str.encode(string1 + "\n"))
    ser1.write(str.encode(string1 + "\n"))


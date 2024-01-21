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


def write_angles(ser0, ser1, legs, debug=False):
    """
    Takes two serial objects and the list of leg angles, and writes to the nine motors controlled by each controller.
    """
    
    left_string = str(int(legs[0][0])) + "," + str(int(legs[0][1])) + "," + str(int(legs[0][2])) + "," + str(int(legs[2][0])) + "," + str(int(legs[2][1])) + "," + str(int(legs[2][2])) + "," + str(int(legs[4][0])) + "," + str(int(legs[4][1])) + "," + str(int(legs[4][2]))
    right_string = str(int(legs[1][0])) + "," + str(int(legs[1][1])) + "," + str(int(legs[1][2])) + "," + str(int(legs[3][0])) + "," + str(int(legs[3][1])) + "," + str(int(legs[3][2])) + "," + str(int(legs[5][0])) + "," + str(int(legs[5][1])) + "," + str(int(legs[5][2]))

    ser0.write(str.encode(left_string + "\n"))
    ser1.write(str.encode(right_string + "\n"))

    if debug == True: print ("Left side " + left_string) 
    if debug == True: print ("Right side " + right_string) 


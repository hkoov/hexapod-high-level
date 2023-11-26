import math

"""
Conventions:
alpha = joint 1 angle
beta = joint 2 angle
gamma = joint 3 angle


length = distance from 



"""



def up_down_degrees (change, range, coxa, femur, tibia, angles):
    """
    This function returns new joint 2 and 3 angles based on the desired height change

    Inputs:
    change: Value between -1 and 1, dictating the height change from 0 (no adjustment)
    range: The maximum change in height (up or down) in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres
    angles: A list of angles containing the following:
        alpha: Current joint 1 angle in degrees
        beta: Current joint 2 angle in degrees
        gamma: Current joint 3 angle in degrees

    Outputs:
    alpha: Same joint 1 angle in degrees
    beta_new_deg: Resultant joint 2 angle in degrees
    gamma_new_deg: Resultant joint 3 angle in degrees

    """
    # Get beta and gamma in radians. 
    beta_rad = angles[1] * math.pi / 180
    gamma_rad = (angles[2] + 25)* math.pi / 180     # Add 25 degrees on to gamma, to allow for the offset of the tip from the tibia
    
    # Calculate the length: distance from joint 2 to the tip
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(gamma_rad))    

    # Calculate theta (angle from joint 2 to tip) and phi (180 degrees - beta - theta)
    theta_rad = math.asin((tibia * math.sin(gamma_rad)) / length)
    phi_rad = math.pi - beta_rad - theta_rad

    # Calculate height and extent based on length and phi
    height = length * math.cos(phi_rad)
    extent = length * math.sin(phi_rad)

    # Change the height based on the change fraction and the range
    height_new = height + change * range

    # This gives us the new length from joint 2 to the tip
    length_new = math.sqrt(height_new**2 + extent**2)

    # Calculate the new joint angles based on the new height and length
    gamma_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    theta_new = math.asin((tibia * math.sin(gamma_new)) / length_new)
    phi_new = math.acos(height_new / length_new)
    beta_new = math.pi - phi_new - theta_new

    # Convert the new joint angles back to degrees
    beta_new_deg = 180 * beta_new / math.pi
    gamma_new_deg = 180 * gamma_new / math.pi - 25  # Now remove the 25 degree offset from the joint angle to get the motor angle

    # Return the new joint angles in degrees
    return [angles[0], beta_new_deg, gamma_new_deg]


def forward_back_degrees (change, range, coxa, femur, tibia, angles):
    """
    This function returns new joint 1, 2, and 3 angles based on the desired forward/back
    movement (i.e., along the Y axis)

    Inputs:
    change: Value between -1 and 1, dictating the forward/back change from 0 (no adjustment)
    range: The maximum change in distance (forward or backward) in millimetres
     
    coxa: Coxa length in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres

    angles: A list of angles containing the following:
        alpha: Current joint 1 angle in degrees
        beta: Current joint 2 angle in degrees
        gamma: Current joint 3 angle in degrees

    
    Outputs:
    alpha_new_deg: Resultant joint 1 angle in degrees
    beta_new_deg: Resultant joint 2 angle in degrees
    gamma_new_deg: Resultant joint 3 angle in degrees

    """
    # Get the angles in radians. 
    alpha_rad = angles[0] * math.pi / 180
    beta_rad = angles[1] * math.pi / 180
    gamma_rad = (angles[2] + 25)* math.pi / 180     # Add 25 degrees on to gamma, to allow for the offset of the tip from the tibia
    
    # Get the starting length: distance from joint 2 to the tip
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(gamma_rad))

    # Calculate theta (angle from joint 2 to tip) and phi (180 degrees - beta - theta)
    theta_rad = math.asin((tibia * math.sin(gamma_rad)) / length)
    phi_rad = math.pi - beta_rad - theta_rad

    # Calculate the extent: distance from joint 1 to the tip in the X/Y plane, as well as the x, y, and xy distances from joint 1 to the tip
    extent = length * math.sin(phi_rad)
    xy_dist = coxa + extent
    x_dist = xy_dist * math.sin(alpha_rad)
    y_dist = xy_dist * math.cos(alpha_rad)

    # Calculate the movement along the y-axis in millimetres
    y_dist_new = y_dist + change * range

    # Now get the new xy_distance
    xy_dist_new = math.sqrt(x_dist ** 2 + y_dist_new ** 2)

    # This gives us the new coxa angle:
    alpha_new = math.acos(y_dist_new / xy_dist_new) # Take the acos of y/xy instead of the asin of x/xy, since that will give us the >90 degree angle for the back leg
    print(y_dist_new)
    print(xy_dist_new)
    print(str(alpha_new / math.pi * 180))
    # Calculate height and extent based on length and phi
    height = length * math.cos(phi_rad)
    extent = length * math.sin(phi_rad) # note that extent = xy_dist_new - coxa

    # Calculate the new length (from joint 2 to the tip)
    extent_new = xy_dist_new - coxa
    length_new = math.sqrt(height ** 2 + extent_new ** 2)

    # Use these to define new joint 2 and 3 angles
    gamma_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    theta_new = math.asin((tibia * math.sin(gamma_new)) / length_new)
    phi_new = math.acos(height / length_new)
    beta_new = math.pi - phi_new - theta_new

    # Convert the new joint angles back to degrees
    alpha_new_deg = 180 * alpha_new / math.pi
    beta_new_deg = 180 * beta_new / math.pi
    gamma_new_deg = 180 * gamma_new / math.pi - 25  # Now remove the 25 degree offset from the joint angle to get the motor angle

    # Return the new joint angles in degrees
    return [alpha_new_deg, beta_new_deg, gamma_new_deg]


def right_left_degrees (change, range, coxa, femur, tibia, angles):
    """
    This function returns new joint 1, 2, and 3 angles based on the desired right/left
    movement (i.e., along the X axis)

    Inputs:
    change: Value between -1 and 1, dictating the right/left change from 0 (no adjustment)
    range: The maximum change in distance (right or left) in millimetres
     
    coxa: Coxa length in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres

    angles: A list of angles containing the following:
        alpha: Current joint 1 angle in degrees
        beta: Current joint 2 angle in degrees
        gamma: Current joint 3 angle in degrees

    
    Outputs:
    alpha_new_deg: Resultant joint 1 angle in degrees
    beta_new_deg: Resultant joint 2 angle in degrees
    gamma_new_deg: Resultant joint 3 angle in degrees

    """
    # Get the angles in radians. 
    alpha_rad = angles[0] * math.pi / 180
    beta_rad = angles[1] * math.pi / 180
    gamma_rad = (angles[2] + 25)* math.pi / 180     # Add 25 degrees on to gamma, to allow for the offset of the tip from the tibia
    
    # Get the starting length: distance from joint 2 to the tip
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(gamma_rad))

    # Calculate theta (angle from joint 2 to tip) and phi (180 degrees - beta - theta)
    theta_rad = math.asin((tibia * math.sin(gamma_rad)) / length)
    phi_rad = math.pi - beta_rad - theta_rad

    # Calculate the extent: distance from joint 1 to the tip in the X/Y plane, as well as the x, y, and xy distances from joint 1 to the tip
    extent = length * math.sin(phi_rad)
    xy_dist = coxa + extent
    x_dist = xy_dist * math.sin(alpha_rad)
    y_dist = xy_dist * math.cos(alpha_rad)

    # Calculate the movement along the y-axis in millimetres
    x_dist_new = x_dist + change * range

    # Now get the new xy_distance
    xy_dist_new = math.sqrt(x_dist_new ** 2 + y_dist ** 2)

    # This gives us the new coxa angle:
    alpha_new = math.acos(y_dist / xy_dist_new) # Take the acos of y/xy instead of the asin of x/xy, since that will give us the >90 degree angle for the back leg


    # Calculate height and extent based on length and phi
    height = length * math.cos(phi_rad)
    extent = length * math.sin(phi_rad) # note that extent = xy_dist_new - coxa

    # Calculate the new length (from joint 2 to the tip)
    extent_new = xy_dist_new - coxa
    length_new = math.sqrt(height ** 2 + extent_new ** 2)

    # Use these to define new joint 2 and 3 angles
    gamma_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    theta_new = math.asin((tibia * math.sin(gamma_new)) / length_new)
    phi_new = math.acos(height / length_new)
    beta_new = math.pi - phi_new - theta_new

    # Convert the new joint angles back to degrees
    alpha_new_deg = 180 * alpha_new / math.pi
    beta_new_deg = 180 * beta_new / math.pi
    gamma_new_deg = 180 * gamma_new / math.pi - 25  # Now remove the 25 degree offset from the joint angle to get the motor angle

    # Return the new joint angles in degrees
    return [alpha_new_deg, beta_new_deg, gamma_new_deg]
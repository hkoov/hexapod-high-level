import math

"""
Conventions:
The centre point is defined as the point in the centre of the body.
    In X and Y, it is located in the centre of the coxa joints, i.e., halfway between joints 1 in the middle two legs
    In Z, it is on the plane going through all the joint 2s

For the rotations, the frame of reference moves with the body 
    E.g. the roll rotation around the Y axis shifts the angle of the X axis around which the subsequent rotation will be performed
    The maths is set out assuming the body remains still and the legs rotate around the origin

"""



def roll (change, range, x_offset, y_offset, coxa, femur, tibia, angles):
    """
    This function returns new joint 1, 2 and, 3 angles based on the desired roll angle

    Inputs:
    change: Value between -1 and 1, dictating the roll change from 0 (no adjustment)
    range: The maximum change in a roll angle (in degrees)
    x_offset: Left/right distance from the centre of the body to joint 1, where left is negative and right is positive 
    y_offset: Forward/backward distance from the centre of the body to joint 1, where forward is positive and backward is negative
    coxa: Coxa length in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres
    angles: A list of angles containing the following:
        alpha: Current joint 1 angle in degrees
        beta: Current joint 2 angle in degrees
        gamma: Current joint 3 angle in degrees

    Outputs:
    alpha: Resultant joint 1 angle in degrees
    beta_new_deg: Resultant joint 2 angle in degrees
    gamma_new_deg: Resultant joint 3 angle in degrees

    Conventions:
    length refers to the distance (in all axes) from joint 2 to the tip of the leg
    total_length refers to the distance (in all axes) from the origin of the robot's body to the tip of the leg
    extent refers to the distance (in X and Y) from joint 2 to the tip of the leg
    total_length refers to the distance (in X and Y) from the origin of the robot's body to the tip of the leg
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

    # Calculate the height. The vertical height of joint 2 is the same as the height of the origin
    height = length * math.cos(phi_rad)

    # Calculate the extent: distance from joint 2 to the tip in the X/Y plane, as well as the x, y, and xy distances from joint 1 to the tip
    extent = length * math.sin(phi_rad)
    xy_dist = coxa + extent
    x_dist = xy_dist * math.sin(alpha_rad)
    y_dist = xy_dist * math.cos(alpha_rad)

    # Now get the total extents and lengths - i.e. from the origin
    x_total = x_dist + x_offset
    y_total = y_dist + y_offset

    extent_total = math.sqrt(x_total ** 2 + y_total ** 2)
    length_total = math.sqrt(extent_total ** 2 + height ** 2)

    # Get the projection of the total length onto the X-Z and Y-Z planes
    xz_length_total = math.sqrt(x_total ** 2 + height ** 2)
    yz_length_total = math.sqrt(y_total ** 2 + height ** 2)

    # Calculate the psi angles: 
    # psi is the angle of the total length relative to the vertical through the origin
    # psi_x is this angle projected onto the X-Z plane
    # psi_y is this angle projected onto the Y-Z plane
    psi = math.acos(height / length_total)
    psi_x = math.acos(height / xz_length_total)
    psi_y = math.acos(height / yz_length_total)

    # Calculate the change in roll angle in degrees
    roll = change * range

    # Now get the new psi_x
    psi_x_new = psi_x + roll

    # This gives us the new height and total x distance:
    height_new = xz_length_total * math.cos(psi_x_new)
    x_total_new = xz_length_total * math.sin(psi_x_new)
    
    # Get the new X and XY distances
    x_dist_new = x_total_new - x_offset
    xy_dist_new = math.sqrt(x_dist_new ** 2 + y_dist ** 2)

    # Calculate the resulting new alpha from this, using the original y_dist
    alpha_new = alpha_rad * math.acos(y_dist / xy_dist_new) / math.acos(y_dist / xy_dist) ## Take the acos of y/xy instead of the asin of x/xy, since that will give us the >90 degree angle for the back leg
    
    # Calculate the new length (from joint 2 to the tip)
    extent_new = xy_dist_new - coxa
    length_new = math.sqrt(height_new ** 2 + extent_new ** 2)

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
    y_dist_new = y_dist - change * range

    # Now get the new xy_distance
    xy_dist_new = math.sqrt(x_dist ** 2 + y_dist_new ** 2)

    # This gives us the new coxa angle:
    alpha_new = alpha_rad * math.acos(y_dist_new / xy_dist_new) / math.acos(y_dist / xy_dist) # Take the acos of y/xy instead of the asin of x/xy, since that will give us the >90 degree angle for the back leg
    
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
    alpha_new = alpha_rad * math.acos(y_dist / xy_dist_new) / math.acos(y_dist / xy_dist)  # Take the acos of y/xy instead of the asin of x/xy, since that will give us the >90 degree angle for the back leg


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
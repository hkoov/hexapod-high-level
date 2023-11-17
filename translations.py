import math

"""
Conventions:
alpha = joint 1 angle
beta = joint 2 angle
gamma = joint 3 angle


length = distance from 



"""



def up_down_degrees (change, range, femur, tibia, beta, gamma):
    """
    This function returns new joint 2 and 3 angles based on the desired height change

    Inputs:
    change: Value between -1 and 1, dictating the height change from 0 (no adjustment)
    range: The maximum change in height (up or down) in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres
    beta: Current joint 2 angle in degrees
    gamma: Current joint 3 angle in degrees

    Outputs:
    beta_new_deg: Resultant joint 2 angle in degrees
    gamma_new_deg: Resultant joint 3 angle in degrees

    """
    # Get beta and gamma in radians. 
    beta_rad = beta * math.pi / 180
    gamma_rad = (gamma + 25)* math.pi / 180     # Add 25 degrees on to gamma, to allow for the offset of the tip from the tibia
    
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
    print(change*range)
    print(((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia)))
    gamma_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    theta_new = math.asin((tibia * math.sin(gamma_new)) / length_new)
    phi_new = math.acos(height_new / length_new)
    beta_new = math.pi - phi_new - theta_new

    # Convert the new joint angles back to degrees
    beta_new_deg = 180 * beta_new / math.pi
    gamma_new_deg = 180 * gamma_new / math.pi - 25  # Now remove the 25 degree offset from the joint angle to get the motor angle

    # Return the new joint angles in degrees
    return [beta_new_deg, gamma_new_deg]
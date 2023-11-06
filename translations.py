import math

"""
Conventions:
alpha = joint 1 angle
beta = joint 2 angle
gamma = joint 3 angle


length = distance from 



"""



def up_down_degrees (change, range, femur, tibia, alpha, beta):
    """
    This function returns new joint 2 and 3 angles based on the desired height change

    Inputs:
    change: Value between -1 and 1, dictating the height change from 0 (no adjustment)
    range: The maximum change in height (up or down) in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres
    alpha: Current joint 2 angle in degrees
    beta: Current joint 3 angle in degrees

    Outputs:
    alpha_new_deg: Resultant joint 2 angle in degrees
    beta_new_deg: Resultant joint 3 angle in degrees

    """
    
    alpha_rad = alpha * math.pi / 180
    beta_rad = (beta + 25)* math.pi / 180
    
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(beta_rad))

    gamma_rad = math.asin((tibia * math.sin(beta_rad)) / length)
    theta_rad = math.pi - alpha_rad - gamma_rad

    height = length * math.cos(theta_rad)
    extent = length * math.sin(theta_rad)

    height_new = height + change * range

    length_new = math.sqrt(height_new**2 + extent**2)

    beta_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    gamma_new = math.asin((tibia * math.sin(beta_new)) / length_new)
    theta_new = math.acos(height_new / length_new)
    alpha_new = math.pi - theta_new - gamma_new

    alpha_new_deg = 180 * alpha_new / math.pi
    beta_new_deg = 180 * beta_new / math.pi - 25

    print(alpha_rad, alpha_new, beta_rad, beta_new)

    return [alpha_new_deg, beta_new_deg]


def lef_right_degrees (change, range, coxa, femur, tibia, alpha, beta, gamma):
    """
    This function returns new joint 2 and 3 angles based on the desired height change

    Inputs:
    change: Value between -1 and 1, dictating the height change from 0 (no adjustment)
    range: The maximum change in height (up or down) in millimetres
    femur: Femur length in millimetres
    tibia: Tibia length in millimetres
    alpha: Current joint 2 angle in degrees
    beta: Current joint 3 angle in degrees

    Outputs:
    alpha_new_deg: Resultant joint 2 angle in degrees
    beta_new_deg: Resultant joint 3 angle in degrees

    """
    
    alpha_rad = alpha * math.pi / 180
    beta_rad = (beta + 25)* math.pi / 180
    
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(beta_rad))

    gamma_rad = math.asin((tibia * math.sin(beta_rad)) / length)
    theta_rad = math.pi - alpha_rad - gamma_rad

    height = length * math.cos(theta_rad)
    extent = length * math.sin(theta_rad)

    height_new = height + change * range

    length_new = math.sqrt(height_new**2 + extent**2)

    beta_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    gamma_new = math.asin((tibia * math.sin(beta_new)) / length_new)
    theta_new = math.acos(height_new / length_new)
    alpha_new = math.pi - theta_new - gamma_new

    alpha_new_deg = 180 * alpha_new / math.pi
    beta_new_deg = 180 * beta_new / math.pi - 25

    print(alpha_rad, alpha_new, beta_rad, beta_new)

    return [alpha_new_deg, beta_new_deg]
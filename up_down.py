import math


async def up_down_degrees (change, range, femur, tibia, alpha, beta):
    alpha_rad = alpha * math.pi / 180
    beta_rad = beta * math.pi / 180
    
    length = math.sqrt(femur**2 + tibia**2 - 2 * femur * tibia * math.cos(beta_rad))

    theta_rad = math.pi - alpha_rad - beta_rad

    height = length * math.cos(theta_rad)
    extent = length * math.sin(theta_rad)

    height_new = height + change * range

    length_new = math.sqrt(height_new**2 + extent**2)

    beta_new = math.acos((length_new**2 - femur**2 - tibia**2) / (-2 * femur * tibia))
    gamma_new = math.asin((tibia * math.sin(beta_new)) / length_new)
    theta_new = math.acos(height_new / length_new)
    alpha_new = math.pi - theta_new - gamma_new

    alpha_new_deg = 180 * alpha_new / math.pi
    beta_new_deg = 180 * beta_new / math.pi

    return alpha_new_deg, beta_new_deg


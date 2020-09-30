# octopusLAB - ESP32board + EDU_SHIELD1

# from utils.pinout import set_pinout
# pinout = set_pinout()

from components.led import Led

led2 = Led(16) # PWM2
led3 = Led(25) # PWM3

relay = Led(17) # PWM1
# octopusLAB - ESP32board + EDU_SHIELD1

# from utils.pinout import set_pinout
# pinout = set_pinout()


# --- leds ---

from components.led import Led

led2 = Led(16) # PWM2
led3 = Led(25) # PWM3

# --- buttons ---
from machine import Pin
from components.button import Button

boot_pin = Pin(0, Pin.IN)
boot_button = Button(boot_pin, release_value=1)

pin34 = Pin(34, Pin.IN)
pin35 = Pin(35, Pin.IN)
# pin36 = Pin(36, Pin.IN)
# pin39 = Pin(39, Pin.IN)
right_button = Button(pin35, release_value=1)
left_button = Button(pin34, release_value=1)

# --- relay ---
relay = Led(17) # PWM1


# --- oled ---
# I2C oled display
from utils.octopus import oled_init
from components.oled import threeDigits

oled = oled_init()

OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

def oled_show(oled, strT="- Thermostat -",strB="octopusLAB 2020",num=123):
    oled.fill(0)
    threeDigits(oled,num,True,True) # num, 0.1, C

    oled.text(strT, OLED_x0, 3)
    oled.hline(0,52,OLEDX-OLED_x0,1)
    oled.text(strB, OLED_x0, OLED_ydown)
    oled.show()


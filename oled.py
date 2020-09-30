# I2C oled display

from utils.octopus import oled_init
from components.oled import threeDigits


# def oled():
#    o = oled_init()
#    return o

oled = oled_init()

OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

def oled_show(oled, strT="Thermostat v.2",strB="octopusLAB 2020",num=123):
    oled.fill(0)
    threeDigits(oled,num,True,True) # num, 0.1, C

    oled.text(strT, OLED_x0, 3)
    oled.hline(0,52,OLEDX-OLED_x0,1)
    oled.text(strB, OLED_x0, OLED_ydown)
    oled.show()

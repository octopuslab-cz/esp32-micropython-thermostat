# octopusLAB - thermostat19 - v.1

from machine import Pin
from time import sleep, sleep_ms
from utils.octopus import w

# import blesync_server
# import blesync_uart.server
# import utils.ble.bluefruit as bf

from config import Config
conf = Config("thermostat")

from utils.octopus_lib import getUid
uID5 = getUid(short=5) 

status = 200

print("OctopusLAB Thermostat")

print("---init---")
tempH = conf.get("tempH")
tempL = conf.get("tempL")
print("tempL|tempH:",tempL,tempH)
# w()

print("---leds---")
from leds import led2, led3
led2.blink(300)
led3.blink(300)

print("---oled---")
from oled import oled, oled_show
oled_show(oled,strB="tempLH " + str(tempL) + " | " + str(tempH),num=status)


print("---buttons---")
from components.button import Button

boot_pin = Pin(0, Pin.IN)
boot_button = Button(boot_pin, release_value=1)

pin34 = Pin(34, Pin.IN)
pin35 = Pin(35, Pin.IN)
# pin36 = Pin(36, Pin.IN)
# pin39 = Pin(39, Pin.IN)

right_button = Button(pin35, release_value=1)
left_button = Button(pin34, release_value=1)



def left_action():
    global status
    led2.value(1)
    status = status - 5
    oled_show(oled,num=status)


def right_action():
    global status
    led3.value(1)
    status = status + 5
    oled_show(oled,num=status)


def clear_action():
    _thread.start_new_thread(tblink, (3,200))
    print("clear_action: ", end = ' ')
    led2.value(0)
    led3.value(0)
    oled.fill(0)    
    sleep(1)
    oled.show()
    print("DONE")


def save_action():
    _thread.start_new_thread(tblink, ())
    print("save_action")



@boot_button.on_press
def boot_button_on_press():
    print('boot_button_on_press')

@boot_button.on_long_press
def boot_button_on_long_press():
    print('boot_button_on_long_press')
    clear_action()

@boot_button.on_release
def boot_button_on_release():
    print('boot_button_on_release')


@right_button.on_press
def right_button_on_press():
    print('right_button_on_press')
    right_action()

@right_button.on_release
def right_button_on_release():
    print('right_button_on_release')
    led3.value(0)


@right_button.on_long_press
def right_button_on_long_press():
    print('right_button_on_long_press')
    save_action()
    led3.blink()
    led3.value(0)


@left_button.on_press
def left_button_on_press():
    print('right_left_on_press')
    left_action()


@left_button.on_release
def left_button_on_release():
    print('left_button_on_release')
    led2.value(0)


@left_button.on_long_press
def left_button_on_long_press():
    print('left_button_on_long_press')
    save_action()
    led2.blink()
    led2.value(0)

# print("BLE")
# devName = 'octopus-t-'+uID5
# print("BLE ESP32 device name: " + devName)
# oled_show(oled,strB = devName)

oled_show(oled,strB="tempLH " + str(tempL) + " | " + str(tempH))

print("---main-loop---")
while True:
    print("temp")
    sleep(10)

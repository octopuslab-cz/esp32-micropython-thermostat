# octopusLAB - thermostat19 - v.1

from time import sleep, sleep_ms
from utils.octopus import w
from ntptime import settime
from machine import RTC
from utils.octopus_lib import get_hhmm,setlocal
from utils.database.influxdb import InfluxDB
# setlocal?

# import blesync_server
# import blesync_uart.server
# import utils.ble.bluefruit as bf

from config import Config
conf = Config("thermostat")

from utils.octopus_lib import getUid
uID5 = getUid(short=5) 

status = 200 # for 20.0 C
statusRelay = 10 # 10=False, 15 True
pause = 10

print("OctopusLAB hermostat")

print("---init---")
tempH = conf.get("tempH")
tempL = conf.get("tempL")
print("save:",tempL,tempH)
# w()

print("---leds---")
from edushield import led2, led3
led2.blink(300)
led3.blink(300)

print("---oled---")
from edushield import oled, oled_show
oled_show(oled,strB="saved: " + str(tempL) + " | " + str(tempH),num=status)


print("---buttons---")
from edushield import boot_button, right_button, left_button

print("---relay---")
from edushield import relay
led2.value(1)
relay.value(1)
sleep(1)
relay.value(0)
led2.value(0)

print("---thermometer---")
from components.iot import Thermometer
tt = Thermometer(32)  # DEV1 pin 
tx = tt.ds.scan()
print(tt.get_temp(0))
# tt.get_temp(1)

print("---wifi-influx---")
def influx_write():
    temp = tt.get_temp()
    print(influx.write(relay=statusRelay,tempset=status/10,temperature=temp))

w()
influx = InfluxDB.fromconfig()
print("imflux write test")
influx_write()


print("---set-time---")
rtc = RTC()
try:
    settime()
    print(get_hhmm(rtc))
    # + 2 h.
    setlocal(2)
    print(get_hhmm(rtc))
except:
    print("err.settime()")



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

# oled_show(oled,strB="tempLH " + str(tempL) + " | " + str(tempH))


print("---main-loop---")

while True:
    temp = tt.get_temp(0)
    print("temp: ", temp)
    
    if (temp*10 < status):
        led3.value(0)
        led2.value(1)
        relay.value(1)
        statusRelay = 15
    else:
        relay.value(0)
        led2.value(0)
        led3.value(1)
        statusRelay = 10
        
        
    timehm = get_hhmm(rtc)
    oled_show(oled,strT="--Temperature--",strB="set: " + str(status/10) + " " + timehm,num=int(temp*10))
    sleep(3)
    oled.fill(0)
    oled.show()
    
    sleep(pause)
    influx_write()

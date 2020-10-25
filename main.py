# octopusLAB - thermostat19 - v.1

from time import sleep, sleep_ms
# from utils.octopus import w
# from utils.wifi_connect import WiFiConnect
from ntptime import settime
from machine import RTC
from utils.octopus_lib import w, get_hhmm,setlocal
from utils.database.influxdb import InfluxDB
# setlocal?

# import blesync_server
# import blesync_uart.server
# import utils.ble.bluefruit as bf

from config import Config
conf = Config("thermostat")
print(gc.mem_free())

from utils.octopus_lib import getUid
uID5 = getUid(short=5) 

status = 200 # for 20.0 C
rOn = 17
rOff = 15
statusRelay = rOff # 10=False, 15 True
pause = 30
mode = 1
tempX = status/10

# mode1: status, mode2 start/stop time

def isTime(debug=True):
    if(debug):
        print("Mode: ",mode)
        print("Time: ",get_hhmm(rtc))
        print("Start/Stop: ",starT, stopT)
    hour = rtc.datetime()[4]    
    return((hour >= starT) and (hour < stopT))

print("OctopusLAB thermostat")

print("---init---")
print(conf.print_all())
tempH = conf.get("tempH")
tempL = conf.get("tempL")
starT = conf.get("starT")
stopT = conf.get("stopT")
timeShift = conf.get("timeShift")
# w()

print("---leds---")
from edushield import led2, led3
led2.blink(300)
led3.blink(300)

print("---oled---")
from edushield import oled, oled_show
oled_show(oled,strB="saved: " + str(tempL) + " | " + str(tempH),num=status)

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

print("---wifi---")
def influx_write():
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    temp = tt.get_temp()
    return influx.write(relay=statusRelay,tempset=tempX,temperature=temp)


net = w()
ip = net.sta_if.ifconfig()[0]
oled_show(oled,strB="IP:" + ip,num=0)
sleep(2)

print("---button-ftp---")
from machine import Pin

btnum = 0
button = Pin(35, Pin.IN)
print("press right button / CTRL+C or continue")
sleep(1)

for i in range(12):
    print("-",end="")
    btnum += button.value()
    sleep(0.2)

if (btnum == 0):
    print("button1 -> start FTP")
    import ftp 

else:
    print("button0 -> continue")
    # ...


print("---buttons---")
from edushield import boot_button, right_button, left_button

print("---wifi-influx---")
influx = InfluxDB.fromconfig()
print("influx write test")
influxOk = influx_write()
print("influx write:", influxOk)
oled_show(oled,strB="influx: " + str(influxOk),num=0)
sleep(1)

print("---set-time---")
rtc = RTC()
try:
    settime()
    print(get_hhmm(rtc))
    # + timeShift  1 / 2 h.
    setlocal(timeShift )
    print(get_hhmm(rtc))
except:
    print("err.settime()")


def left_action():
    global status
    led2.value(1)
    status = status - 5
    oled_show(oled,strB="M" + str(mode) + " " + timehm,num=status)


def right_action():
    global status
    led3.value(1)
    status = status + 5
    oled_show(oled,strB="M" + str(mode) + " " + timehm,num=status)


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
    global mode
    mode = 2
    oled_show(oled,strT="--- Mode ---",strB="set: " + str(mode) + " " + timehm,num=int(temp*10))
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
    global mode
    mode = 1
    oled_show(oled,strT="--- Mode ---",strB="set: " + str(mode) + " " + timehm,num=int(temp*10))
    led2.blink()
    led2.value(0)

# print("BLE")
# devName = 'octopus-t-'+uID5
# print("BLE ESP32 device name: " + devName)
# oled_show(oled,strB = devName)

# oled_show(oled,strB="tempLH " + str(tempL) + " | " + str(tempH))


print("---main-loop---")

while True:
    tempX = status/10 # treshold
    if mode == 2:
       if isTime():
          tempX = tempH
       else:
          tempX = tempL
    
    temp = tt.get_temp(0)
    print("temp/tempx: ", temp, tempX)
    
    if (temp < tempX):
        led3.value(0)
        led2.value(1)
        relay.value(1)
        statusRelay = rOn
    else:
        relay.value(0)
        led2.value(0)
        led3.value(1)
        statusRelay = rOff
        
        
    timehm = get_hhmm(rtc)
    oled_show(oled,strT="--Temperature--",strB="set: " + str(tempX) + " " + timehm,num=int(temp*10))
    sleep(3)
    oled.fill(0)
    oled.show()
    
    sleep(pause)
    influx_write()

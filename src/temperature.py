from sense_hat import SenseHat
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import time
import threading
import os
import subprocess
import json

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9

# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
    offset = val * 15
    for p in range(offset, offset + 15):
        xt = p % 3
        yt = (p-offset) // 3
        sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)

# Gets the temperatures
def get_temperatures():
    temp = sense.get_temperature()
    humidity = sense.get_humidity() 
    pressure = sense.get_pressure() 

    calctemp = 0.0071 * temp * temp + 0.86 * temp - 10.0
    calchum = humidity * (2.5 - 0.029 * temp)

    print(calctemp)
    print(calchum)

    show_number(int(calctemp), 0, 0, 255)

    message = {}
    message['temperature'] = calctemp
    message['humidity'] = calchum
    message['pressure'] = pressure
    message['clientid'] = os.environ['CLIENTID']
    message['date'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    messageJson = json.dumps(message)

    myMQTTClient.publish("temperature_topic/house", messageJson, 0)
    

################################################################################
# MAIN
sense = SenseHat()
sense.clear()

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient(os.environ['CLIENTID'])
myMQTTClient.configureEndpoint(os.environ['HOSTNAME'], 8883)
myMQTTClient.configureCredentials(os.environ['CACERTIFICATE'], os.environ['PRIVATEKEY'], os.environ['CLIENTCERTIFICATES'])
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()

while True:
    get_temperatures()
    time.sleep(os.environ['INTERVAL'])

myMQTTClient.disconnect()
sense.clear()
#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

###### pin assign
#PCF8591 --------- Raspberry pi3
# SDA ------------ GPIO2/SDA1
# SCL ------------ GPIO3/SCL1
# VCC ------------- 3.3V
# GND ------------- GND
#
######

# Description
# in this program, Raspberry pi read a variable registers value(0-255) on PCF8591 default. And 
# Output to LED which is on PCF8591 using Digital analog converter.

import wiringpi
import time
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

from PCF8591 import PCF8591

def sensordatawrite(path,sensordate):
    now=date.today()
    tmp=[now.year, now.month, now.day, now.hour,sensordata]
    with open(path, mode='a') as f:
        f.write(",".join(map(str,tmp)))
    return

Sensor1_outputpath="Sensor1_ourput.csv"
Sensor2_outputpath="Sensor2_ourput.csv"

if __name__ == "__main__":
    
    pcf8591 = PCF8591(0x48)
    MotionSensor_pin = 1 #wiringpi number see :https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    wiringpi.pinMode( MotionSensor_pin,0)# set as input pin
    
    csv_colmnsname=["year","month","hour","sensor_value"]
    #Init outputfile
    with open(Sensor1_outputpath, mode='a') as f:
                f.write(",".join(csv_colmnsname))
    with open(Sensor2_outputpath, mode='a') as f:
                f.write(",".join(csv_colmnsname))
    
    
    while True:
        currentday=date.today().strftime("%Y_%m_%d")
        while True: #1day loop
            ##check the day is passed?
            if currentday != date.today().strftime("%Y_%m_%d"):
                break
            
            sensordata1=[]
            sensordata2=[]
            StartTimeH=datetime.now()
            while True: #1hour loop
                #check pass 1hour or not 
                if (datetime.now()-StartTimeH).total_seconds()>3600:
                    break
                # read infrared sensor value
                sensordata1.append(wiringpi.digitalRead(MotionSensor_pin))
            
                #PCF8591 processing AD conversion
                value=pcf8591.analogRead0()
                sensordata2.append(value)
                pcf8591.DAoutput(value)
                #print(value)
                time.sleep(1)
                
            #### END 1hour loop ####
            sensordata1Series=pd.Series(sensordata1)
            sensordata2Series=pd.Series(sensordata2)
            
            sensordatawrite(Sensor1_outputpath,sensordata1Series.mean())
            sensordatawrite(Sensor2_outputpath,sensordata2Series.mean())
            
                
        #### END 1day loop ####
        

    


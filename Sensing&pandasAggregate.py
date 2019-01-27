#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

###### pin assign
#PCF8591 --------- Raspberry pi3
# SDA ------------ GPIO2/SDA1
# SCL ------------ GPIO3/SCL1
# VCC ------------- 3.3V
# GND ------------- GND
#
# GPIO 1 (18)------ IR sensor1
# GPIO 4 (23)------ IR sensor2
# GPIO 5 (24)------ IR sensor3

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

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def sensordatawrite(path,sensordata,worksheet):
    tmp=[datetime.now().strftime("%Y_%m_%d %H:%M:%S"),round(sensordata,3)]
    
    try:
        #write csv
        with open(path, mode='a') as f:
            f.write(",".join(map(str,tmp))+"\n")
        
        #write spread sheet
            worksheet.append_row(tmp)
    except ZeroDivisionError as e:
        print(e)
        
    return

Sensor_outputpaths=[
    "IRSensor1_ourput.csv",
    "IRSensor2_ourput.csv",
    "IRSensor3_ourput.csv",
    "Sensor4_ourput.csv"]


if __name__ == "__main__":
    
    #init pct8591
    pcf8591 = PCF8591(0x48)
    MotionSensor1_pin = 1 #wiringpi number see :https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    MotionSensor2_pin = 4
    MotionSensor3_pin = 5
    wiringpi.pinMode( MotionSensor1_pin,0)# set as input pin
    wiringpi.pinMode( MotionSensor2_pin,0)
    wiringpi.pinMode( MotionSensor3_pin,0)
    
    #init google spreadsheet
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    gc = gspread.authorize(credentials)
    workbook1 = gc.open('Sensor1_output')
    workbook2 = gc.open('Sensor2_output')
    worksheets=[]
    worksheets.append(workbook1.worksheet("IRsensor1"))
    worksheets.append(workbook1.worksheet("IRsensor2"))
    worksheets.append(workbook1.worksheet("IRsensor3"))
    worksheets.append(workbook2.sheet1)
    
    csv_colmnsname=["time","sensor_value"]
    
    #Init outputfile
    #for Sensor_outputpath in Sensor_outputpaths:
    #    with open(Sensor_outputpath, mode='a') as f:
    #        f.write(",".join(csv_colmnsname)+"\n")
    
    
    
    while True:
        currentday=date.today().strftime("%Y_%m_%d")
        while True: #1day loop
            ##check the day is passed?
            if currentday != date.today().strftime("%Y_%m_%d"):
                break
            
            sensordata1=[]
            sensordata2=[]
            sensordata3=[]
            sensordata4=[]
            StartTimeH=datetime.now()
            while True: #1hour loop
                #check pass 5min or not 
                if (datetime.now()-StartTimeH).total_seconds()>30:
                    break
                
                # read infrared sensor value
                sensordata1.append(wiringpi.digitalRead(MotionSensor1_pin))
                sensordata2.append(wiringpi.digitalRead(MotionSensor2_pin))
                sensordata3.append(wiringpi.digitalRead(MotionSensor3_pin))
            
                #PCF8591 processing AD conversion
                value=pcf8591.analogRead0()
                sensordata4.append(value)
                pcf8591.DAoutput(value)
                
                print("IR1:{0} IR2:{1} IR3:{2} AD:{3}".format(sensordata1[-1],sensordata2[-1],sensordata3[-1],sensordata4[-1]))
                time.sleep(1)
                
            #### END 1hour loop ####
            sensordataSeries=[]
            sensordataSeries.append(pd.Series(sensordata1))
            sensordataSeries.append(pd.Series(sensordata2))
            sensordataSeries.append(pd.Series(sensordata3))
            sensordataSeries.append(pd.Series(sensordata4))
            
            print("write data")
            for its_outputpath,its_worksheet,its_data in zip(Sensor_outputpaths,worksheets,sensordataSeries):
                sensordatawrite(its_outputpath,its_data.mean(),its_worksheet)
            
            
                
        #### END 1day loop ####
        

    



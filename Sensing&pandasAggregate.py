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
from datetime import datetime
import numpy as np


class PCF8591:
    def __init__(self, addr):
        wiringpi.wiringPiSetup() #setup wiringpi

        self.i2c = wiringpi.I2C() #get I2C
        self.dev = self.i2c.setup(addr) #setup I2C device

    def LED_ON(self):
        self.i2c.writeReg8(self.dev, 0x40, 0xFF)
        
    def LED_OFF(self):
        self.i2c.writeReg8(self.dev, 0x40, 0x00)
        
    def DAoutput(self,value):
        self.i2c.writeReg8(self.dev, 0x40, value)
        
    def analogRead0(self):
        self.i2c.writeReg8(self.dev, 0x48,0x40)
        self.i2c.readReg8(self.dev,0x48)    #read dummy
        return self.i2c.readReg8(self.dev,0x48)
        
    def analogRead1(self):
        self.i2c.writeReg8(self.dev, 0x48,0x41)
        self.i2c.readReg8(self.dev,0x48)    #read dummy
        return self.i2c.readReg8(self.dev,0x48)
        
    def analogRead2(self):
        self.i2c.writeReg8(self.dev, 0x48,0x42)
        self.i2c.readReg8(self.dev,0x48)    #read dummy
        return self.i2c.readReg8(self.dev,0x48)
    def analogRead3(self):
        self.i2c.writeReg8(self.dev, 0x48,0x43)
        self.i2c.readReg8(self.dev,0x48)    #read dummy
        return self.i2c.readReg8(self.dev,0x48)
    def analogRead(self,pin):
        self.i2c.writeReg8(self.dev, 0x48,0x40+pin)
        self.i2c.readReg8(self.dev,0x48)    #read dummy
        return self.i2c.readReg8(self.dev,0x48)

if __name__ == "__main__":
    
    pcf8591 = PCF8591(0x48)
    MotionSensor_pin = 1 #wiringpi number see :https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    wiringpi.pinMode( MotionSensor_pin,0)# set as input pin
    
    StartTime=datetime.now()
    soundlist=[]
    while True:
        """
        if (datetime.now()-StartTime).total_seconds()>10:
                break
        """
        value=pcf8591.analogRead0()
        soundlist.append(value)
        pcf8591.DAoutput(value)
        #print(value)
        if len(soundlist)>40:
            print(np.mean(soundlist))
            soundlist=[]
        #print(wiringpi.digitalRead(MotionSensor_pin))
        #time.sleep(0.1)
    print(len(soundlist))

    


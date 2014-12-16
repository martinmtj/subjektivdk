#!/usr/bin/python

import os
import glob
import time
import RPi.GPIO as GPIO
import sqlite3
#initialize the device  
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

time.sleep(5)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c

#print (read_temp())
pictime = time.strftime('%Y-%m-%d %H:%M:%S'')
location = 'Indoor'
indoortemp = (read_temp())

print indoortemp
conn = sqlite3.connect('datalog.db')
c = conn.cursor()
c.execute("INSERT INTO temp VALUES(?,?,?)",(pictime, location, indoortemp))
conn.commit()
conn.close()


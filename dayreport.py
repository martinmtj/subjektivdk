#!/usr/bin/python

import time
import picamera
import datetime
import os
import glob
import RPi.GPIO as GPIO

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

indoortemp = (read_temp())

pictime = time.strftime('%Y%m%d-%H%M') # Timestamp
picurl = ('/home/pi/camera/' + pictime + '.jpg') # Set complete url for picture
upload = ('wput -B -R -q ' + picurl + ' ftp://USER:PASSWORD@voresserver.dk/sommerhus/') # Shell command for uploading picture to remote ftp server
with picamera.PiCamera() as camera: # Start the picamera function
	camera.resolution = (1295, 975) # Highest resolution using the 2x2 bin mode
	camera.hflip = True 
	camera.vflip = True
	camera.annotate_text = (pictime + " - " + indoortemp + "c") # Annotating timestamp on the picture
	camera.start_preview()
	time.sleep(1) # Camera warm-up
	camera.capture(picurl) # Saved picture 
	print (time.strftime('%Y%m%d-%H%M%S') + '-> Picture saved here: ' + picurl)
	os.system(upload) # ftp upload
	print (time.strftime('%Y%m%d-%H%M%S') + '-> Uploaded to remote server')
	print (time.strftime('%Y%m%d-%H%M%S') + '-> Ready')


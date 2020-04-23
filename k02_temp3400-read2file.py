#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import time
import datetime

base_dir = "/sys/bus/w1/devices"
sensor_dir = base_dir + "/10*"
sensor_list_long = glob.glob(sensor_dir)
trim_letter = sensor_dir.find("10")
sensor_list = [sensor[trim_letter:] for sensor in sensor_list_long]
#sensor_list = [sensor_list[0],sensor_list[0],sensor_list[0],sensor_list[0]]
#print(sensor_list)
#print('end intro')

sensor_count = len(sensor_list)
#print(sensor_count)

## reads the output of the sensor file in /sys/bus/w1/devices/10*/w1_slave
def read_temp_raw():
    #print(sensor_list)
    #print (device_file[0])
    #print('Heyhey')
    f1 = open(device_file, 'r')
    temp_raw = f1.readlines()
    f1.close()
    return temp_raw

## transforms one line of read_temp_raw to timestamp and temprature (##.#)
def read_temp():
    lines = read_temp_raw()
    #print(lines)
    while lines[0].strip()[-3:] != 'YES': 
        time.sleep(0.2)
        lines = read_temp_raw()
        #print(lines)
    equals_pos = lines[1].find('t=')
    timestamp = time.strftime("%y-%m-%d %H:%M:%S")

    temp = round(float(lines[1][equals_pos+2:])/1000, 1)
    
    return timestamp, temp

## writes output for each sensor (deviceid, timestamp, temp) to file and stdout
fobj = open("/home/dieter/code/temp/temp-datscha3S_topnew.txt", "a")
fobj_old = open("/home/dieter/code/temp_old/temp-datscha3S_new.txt", "a")

# ab hier Multithreading umsetzen
for sensor in sensor_list:
    #print(len(sensor))
    device_folder = base_dir + "/" + str(sensor)
    #print(device_folder)
    device_file = device_folder + "/w1_slave"
    #print(device_file)
    #print('Hey')
    tempdata = read_temp()
    #print(sensor + ";" + str(tempdata[0]) + ";" + str(tempdata[1]) + "\n")
    fobj.write(sensor + ";" + str(tempdata[0]) + ";" + str(tempdata[1]) + "\n")
    #fobj_old.write
fobj.close()

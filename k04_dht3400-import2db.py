#!/usr/bin/python
# -*- coding: utf-8 -*-

#import os
import glob
import time
import datetime as dt
import netrc
#import sqlite3 as lite
import sys
#import csv
import pandas as pd
#import mysql.connector as mariadb
import MySQLdb as mariadb




#timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

## set up database connection
def db_connect():
    try:
        host = 'localhost'
        cred = netrc.netrc().authenticators(host)
        #print(cred)
        mdb_conn = mariadb.connect(host, cred[0], cred[2], 'meteo')

    except:
        print("I am unable to connect to mariadb database meteo!")

    return mdb_conn

#importdata = pd.DataFrame()

mdb_conn = db_connect()

mcursor_parameter = mdb_conn.cursor()
sql_select_query_parameter = "SELECT * FROM parameter;"
mcursor_parameter.execute(sql_select_query_parameter)
mrecords_parameter = mcursor_parameter.fetchall()

#testing
print(mrecords_parameter)
#sys.exit("Test-Stop: parameters list from db")


<<<<<<< HEAD
importdata = pd.read_csv("~/data/datscha/all/am2601-datscha_all_test.txt", sep=";", header=None, names=['parameter', 'sensor', 'timestamp', 'measure'])
=======

print(importdata)

for rows_importdata in importdata:
    print(rows_importdata[0])
>>>>>>> 73cb2b5ad4803876f4ddedee618bc50291407160


for rows_parameter in mrecords_parameter:
    #print(rows_parameter[0])
    #print(importdata['sensor'])#==rows_parameter[0])
    is_parameter = importdata['parameter']==rows_parameter[0]
    importdata_parameter = importdata[is_parameter]

    #testing
    #print("list:", importdata_parameter['timestamp'])
    #print(importdata_parameter)
    continue

    mcursor_measurement = mdb_conn.cursor()
    sql_select_query_measurement = """SELECT MAX(measuredatetime) FROM measurement WHERE sensor_id = %s;"""
    mcursor_measurement.execute(sql_select_query_measurement, (rows_sensor[0],))

    mrecords_measurement = mcursor_measurement.fetchone()

    mcursor_measurement_insert = mdb_conn.cursor()

    for rows_import in importdata_sensor.itertuples():
        #print(rows_import)
        sql_insert_measurement = """INSERT INTO measurement (sensor_id, parameter_id, measuredatetime, measure) VALUES (%s, %s, %s, %s);"""
        inserttuple = (rows_sensor[0], 1, rows_import[2], rows_import[3])
        
        if mrecords_measurement[0] == None:
            #print("NONE!!")    
            #print("inserttuple",inserttuple)
            mcursor_measurement_insert.execute(sql_insert_measurement, inserttuple)
        elif mrecords_measurement[0] < dt.datetime.strptime(rows_import[2], '%y-%m-%d %H:%M:%S'):
            #print(rows_import[2])
            mcursor_measurement_insert.execute(sql_insert_measurement, inserttuple)
        else:
            #print("else")
            pass

        mdb_conn.commit()

        
    #print(importdata_sensor.head(3))
    #print(importdata_sensor['timestamp'].max())



mdb_conn.close()

# with open ('temp-datscha3S_topnew_test.txt','r') as csvfile:
#     input_data = csv.reader(csvfile, delimiter=';')
#     #n=0
#     for row in input_data:
#         #n=n+1
#         #x.append(n)
#         #x.append(row[1])
#         timestamp = datetime.datetime.strptime(row[1],'%y-%m-%d %H:%M:%S')#.timetuple()
#         temp = float(row[2])
#         print temp, temp-1
#         if row[0]=='10-000802a827d4':
#             sensorid = int(2)
#         elif row[0]=='10-000802b58146':
#             #print '58146'
#             sensorid = int(1)
#         elif row[0]=='10-000802a8876f':
#             #print '8876f'
#             sensorid = int(3)
#         else:
#             print 'nein!!!!'

#         print sensorid, timestamp, temp

#         mcursor.execute("INSERT INTO temps (sensorid, timestamp, temp) VALUES (?, ?, ?)", (sensorid, timestamp, temp))
                                                        




# ## reading actuall temperature of two sensors
# def read_temp_raw():
#     #f1 = open(device_file[0], 'r')
#     #lines1 = f1.readlines()
#     #f1.close()
#     #f2 = open(device_file[1], 'r')
#     #lines2 = f2.readlines()
#     #f2.close()
#     #return lines1 + lines2

#     f = open(device_file, 'r')
#     lines = f.readlines()
#     f.close()
#     return lines

# ## extracting needed information
# def read_temp():
#     lines = read_temp_raw()
#     #while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
#     while lines[0].strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = read_temp_raw()
#     equals_pos = lines[1].find('t=')
#     if equals_pos != -1:#lines[1].find('t='), lines[3].find('t=')
#         temp_string = lines[1][equals_pos+2:]
#         temp_c = float(temp_string) / 1000.0
#         ts = time.time()
#         timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        

#         #.isoformat()
#         #timestamp = time.strftime("%y-%m-%d %H:%M:%S")
#         #timestamp2 = datetime.datetime.now()
#         #timestamp3 = datetime.datetime('%Y-%m-%d %H:%M:%S')
#         #c = conn.cursor()
#         print(timestamp)
#         #print(timestamp2)
#         #print(timestamp3)

#         #mcursor.execute("INSERT INTO 1170_wozi (timestamp, temp) VALUES (?, ?)", (timestamp2, temp_c))
#         #time.sleep(10)
#         mcursor.execute("""INSERT INTO 1170_wozi (timest, temp) VALUES (%s, %s)""", (timestamp, temp_c))
#         mariadb_connection.commit()
#         return timestamp, temp_c


# ##print results
# read_temp()

# ##close cursor and sqlite dbconnection
# #conn.close()

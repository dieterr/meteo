#!/usr/bin/python
# -*- coding: utf-8 -*-

import netrc
import pandas as pd
from pandas import read_sql as rsq
import numpy as np 
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import decimal
import sys

## set up database connection
def db_connect():
    try:
        host = 'localhost'
        cred = netrc.netrc().authenticators(host)
        #print(cred[0],cred[2])
        url_object = URL.create("mysql+pymysql",
            username=cred[0],
            password=cred[2],
            host=host,
            database='meteo')
        engine = create_engine("mysql+pymysql://meteo:8sR9eEVtuY2Xsj5sm1B8@127.0.0.1:3306/meteo")

    except:
        print("I am unable to connect to mariadb database meteodb!")

    return engine


def read_db_all(lhb, lhe):
    df_all = rsq("SELECT measuredatetime, measure FROM measurement WHERE parameter_id = 1 AND isDeleted = 0 AND measuredatetime BETWEEN NOW() - INTERVAL %s HOUR AND NOW() - INTERVAL %e HOUR ORDER BY measuredatetime;" %(lhb, lhe), engine)
    df_all.columns = ['measuredatetime', 'temp']
    return df_all


def read_db_hours(id, lhb, lhe):
    df = rsq("SELECT measuredatetime, measure FROM measurement WHERE parameter_id = 1 AND sensor_id = %i AND isDeleted = 0 AND measuredatetime BETWEEN NOW() - INTERVAL %s HOUR AND NOW() - INTERVAL %e HOUR ORDER BY measuredatetime;" %(id, lhb, lhe), engine)
    df.columns = ['measuredatetime', 'temp']
    return df

def statistics(data):
    min = np.min(data['temp'])
    max = np.max(data['temp'])
    mean = round(np.mean(data['temp']),1)

    return min, max, mean

def draw_tempData(now,old):
    if timeSequ > 7:
        # computing a 3 hour rolling average for more than 7 days
        data_now['rolling'] = now.temp.rolling(12).mean()
        now.plot(x='measuredatetime', y='rolling', color=sensorList[i][1], ax=axt, label=i)
        #print(data_now['rolling'])
    else:
        # use orignal data
        now.plot(x='measuredatetime', y='temp', color=sensorList[i][1], ax=axt, label=i)

    plt.hlines(statistics(data_now)[0], np.min(data_now['measuredatetime']), np.max(data_now['measuredatetime']), linestyle = '--', color = sensorList[i][1])
    plt.hlines(statistics(data_now)[1], np.min(data_now['measuredatetime']), np.max(data_now['measuredatetime']), linestyle = 'solid', color = sensorList[i][1])
    plt.hlines(statistics(data_now)[2], np.min(data_now['measuredatetime']), np.max(data_now['measuredatetime']), linestyle = ':', color = sensorList[i][1])
    min_text = 'Min. ' + format(round(statistics(data_now)[0],1), '.1f') + ' (' + format(round(statistics(data_now)[0] - statistics(data_old)[0],1), '.1f') + ')'
    max_text = 'Max. ' + format(round(statistics(data_now)[1],1), '.1f') + ' (' + format(round(statistics(data_now)[1] - statistics(data_old)[1],1), '.1f') + ')'
    mean_text = 'Mw. ' + format(round(statistics(data_now)[2],1), '.1f') + ' (' + format(round(statistics(data_now)[2] - statistics(data_old)[2],1), '.1f') + ')'
    plt.text(np.min(data_now['measuredatetime']), np.min(data_now['temp'])-(range_all / 18), min_text, color = sensorList[i][1], bbox = props)
    plt.text(np.max(data_now['measuredatetime']), np.max(data_now['temp'])+(range_all / 18), max_text, color = sensorList[i][1], bbox = props, ha= 'right')
    plt.text(np.mean(data_now['measuredatetime']), statistics(data_now)[2]+(range_all / 28), mean_text, color = sensorList[i][1], bbox = props, ha = 'center')
    return


#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#print('Argument List1:', str(sys.argv[1]))

#Input days
timeSequ = int(sys.argv[2])
#print('timesequ: ', timeSequ)

likedHours1Begin = timeSequ * 24
likedHours1End = 0 
likedHours2Begin = timeSequ * 24 * 2
likedHours2End = timeSequ * 24

engine = db_connect()

data_all = read_db_all(likedHours1Begin, likedHours1End)

stat = statistics(data_all)

min_all = stat[0]
max_all = stat[1]

range_all = max_all - min_all

#print("min: ",min_all,"max: ",max_all)

sensorList = {"out":[1,"m"],"in":[2,"g"],"workshop":[3,"b"]}

axt = plt.gca()

props = dict(boxstyle='round', facecolor='white', edgecolor='white', alpha=0.7)

for i in sensorList:
    #print("data_"+str(sensorList[i][1]))
    data_now = read_db_hours(sensorList[i][0], likedHours1Begin, likedHours1End)
    data_old = read_db_hours(sensorList[i][0], likedHours2Begin, likedHours2End)
    #data_now['roll'] = data_now['temp'].rolling(12).mean
    #print(data_now_roll)
    #print(data_now)

    #print(statistics(data_now))
    #print("now min: ",statistics(data_now)[0])
    #if timeSequ > 7:
    #    data_now.plot(x='measuredatetime', y='temp', color=sensorList[i][1], ax=axt, label=i)
    #else:
    draw_tempData(data_now,data_old)
    #data_now.plot(x='measuredatetime', y='temp', color=sensorList[i][1], ax=axt, label=i)
    
range_all = max_all - min_all
range_hours = timeSequ * 24


d_fmt = mdates.DateFormatter('%d.%m.%Y')
h_fmt1 = mdates.DateFormatter('%H:%M')
h_fmt2 = mdates.DateFormatter('%H'+' h')

if timeSequ <= 2:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(interval = 2*timeSequ)
    titletxt = 'die letzten '+str(range_hours)+' Stunden:'
    axt.xaxis.set_major_locator(hours)
    axt.xaxis.set_major_formatter(h_fmt1)
elif timeSequ <= 14:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(byhour=[6,12,18])
    titletxt = 'die letzten '+str(timeSequ)+' Tage:'
    axt.xaxis.set_major_locator(days)
    axt.xaxis.set_major_formatter(d_fmt)
else:
    titletxt = 'die letzten '+str(timeSequ)+' Tage:'

plt.title(titletxt)
plt.xlabel(' ')
#plt.xticks([])
plt.ylabel('Temperatur (' + u'\N{DEGREE SIGN}' + 'C)')
axt.get_legend().remove()
#ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3)


if min_all > 0:
    axt.set_ylim(0)

#plt.axhline(0, color = 'k', linewidth = 0.5)
#plt.text(np.min(data_w['measuredatetime']), mean_w+(range_all / 28)+(timesequ/10), "GitTest", color = 'k', bbox = props, ha = 'right')

pltname = '/home/dieter/temp'+str(timeSequ)+'.png'
plt.savefig(pltname)

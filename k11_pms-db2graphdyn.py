#!/usr/bin/python
# -*- coding: utf-8 -*-

import netrc
from pandas import read_sql_query as pdrsq
import numpy as np 
import MySQLdb as mariadb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import decimal
import sys

## set up database connection
def db_connect():
    try:
        host = 'kuerbis04'
        host_ip = '192.168.0.13'
        cred = netrc.netrc().authenticators(host)
        mdb_conn = mariadb.connect(host_ip, cred[0], cred[2], 'meteo')

    except:
        print("I am unable to connect to mariadb database tempdb!")

    return mdb_conn

def read_db_hours(id, ti):
    df = pdrsq("SELECT measuredatetime, measure FROM measurement WHERE parameter_id = %i AND sensor_id = 6 ORDER BY measuredatetime DESC LIMIT %s;" %(id, ti), mdb_conn)
    df.columns = ['measuredatetime', 'temp']
    #print(df)
    return df


#def



#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#print('Argument List1:', str(sys.argv[1]))

#Input days
timesequ = int(sys.argv[1])
#print('timesequ: ', timesequ)

likedhours1 = timesequ * 24 * 4 
likedhours = [str(likedhours1), str(likedhours1)+','+str(likedhours1)]
#print('test', likedhours)
#mdb_conn = None
mdb_conn = db_connect()
#print(mdb_conn)
##print results
#likedhours = ['96', '96,96']
#print('orig: ',likedhours)



##get data
id = 4
data_pm10 = read_db_hours(id, likedhours[0])
data_pm10_b24 = read_db_hours(id, likedhours[1])

id = 5
data_pm25 = read_db_hours(id, likedhours[0])
data_pm25_b24 = read_db_hours(id, likedhours[1])

id = 6
data_pm100 = read_db_hours(id, likedhours[0])
data_pm100_b24 = read_db_hours(id, likedhours[1])


#print(data_pm10)
#print(data_pm25)

#data_pm10_array() = np.asarray(data_pm10)
#export txt-files
#data_pm10_array.tofile('/home/dieter/data/temp-i.txt',sep=';')

## calculate max & mean
max_pm10 = np.max(data_pm10['temp'])
max_pm25 = np.max(data_pm25['temp'])
max_pm100 = np.max(data_pm100['temp'])
max_pm10_b24 = np.max(data_pm10_b24['temp'])
max_pm25_b24 = np.max(data_pm25_b24['temp'])
max_pm100_b24 = np.max(data_pm100_b24['temp'])
mean_pm10 = np.mean(data_pm10['temp'])
mean_pm25 = np.mean(data_pm25['temp'])
mean_pm100 = np.mean(data_pm100['temp'])
mean_pm10_b24 = np.mean(data_pm10_b24['temp'])
mean_pm25_b24 = np.mean(data_pm25_b24['temp'])
mean_pm100_b24 = np.mean(data_pm100_b24['temp'])
min_pm10 = np.min(data_pm10['temp'])
min_pm25 = np.min(data_pm25['temp'])
min_pm100 = np.min(data_pm100['temp'])
min_all = np.min([min_pm10, min_pm25, min_pm100])
max_all = np.max([max_pm10, max_pm25, max_pm100])

range_all = max_all - min_all
range_hours = timesequ * 24
#print(range_all)
#print decimal('66.66666666666').quantize(decimal('1e-4'))

#print(mean_pm10)
#print("Max o: ")
#print(max_pm25)
#print("Max i: ")
#print(max_pm10)



d_fmt = mdates.DateFormatter('%d.%m.%Y')
h_fmt1 = mdates.DateFormatter('%H:%M')
h_fmt2 = mdates.DateFormatter('%H'+' h')
#print data_pm10
#print data_pm25
#max_pm10_txt = "Max (Innen): " + max_pm10 + " °C"
ax = plt.gca()
data_pm10.plot(x='measuredatetime', y='temp', color="y", ax=ax, label='PM1')
data_pm25.plot(x='measuredatetime', y='temp', color="c", ax=ax, label='PM2.5')
data_pm100.plot(x='measuredatetime', y='temp', color="r", ax=ax, label='PM10')
#data_pm10.setlabel('Innen')

if timesequ <= 1:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(interval = 4*timesequ)
    titletxt = 'die letzten '+str(range_hours)+' Stunden:'
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt1)
elif timesequ <= 2:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(interval = 2*timesequ)
    titletxt = 'die letzten '+str(range_hours)+' Stunden:'
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt1)
elif timesequ <= 7:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(byhour=[6,12,18])
    titletxt = 'die letzten '+str(timesequ)+' Tage:'
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(d_fmt)
else:
    days = mdates.DayLocator(interval = 3)
    hours = mdates.HourLocator(byhour=[6,12,18])
    titletxt = 'die letzten '+str(timesequ)+' Tage:'
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(d_fmt)
#    ax.xaxis.set_maxor_locator(hours)
#    ax.xaxis.set_maxor_formatter(h_fmt2)

plt.title(titletxt)
plt.xlabel('Zeit')
plt.ylabel('Konzentration (µg/m³' + ')')
ax.get_legend().remove()
props = dict(boxstyle='round', facecolor='white', edgecolor='white', alpha=0.7)
#ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3)


plt.hlines(np.max(data_pm10['temp']), np.min(data_pm10['measuredatetime']), np.max(data_pm10['measuredatetime']), linestyle = '--', color = 'y')
max_pm10_text = 'Max. ' + format(round(max_pm10,1), '.1f') + ' (' + format(round(max_pm10 - max_pm10_b24,1), '.1f') + ')'
plt.text(np.min(data_pm10['measuredatetime']), np.max(data_pm10['temp'])-(range_all / 18), max_pm10_text, color = 'y', bbox = props)

plt.hlines(np.max(data_pm25['temp']), np.min(data_pm25['measuredatetime']), np.max(data_pm25['measuredatetime']), linestyle = '--', color = 'c')
max_pm25_text = 'Max. ' + format(round(max_pm25,1), '.1f') + ' (' + format(round(max_pm25 - max_pm25_b24,1), '.1f') + ')'
plt.text(np.min(data_pm25['measuredatetime']), np.max(data_pm25['temp'])-(range_all / 18), max_pm25_text, color = 'c', bbox = props, ha = 'left')

plt.hlines(np.max(data_pm100['temp']), np.min(data_pm100['measuredatetime']), np.max(data_pm100['measuredatetime']), linestyle = '--', color = 'r')
max_pm100_text = 'Max. ' + format(round(max_pm100,1), '.1f') + ' (' + format(round(max_pm100 - max_pm100_b24,1), '.1f') + ')'
plt.text(np.min(data_pm100['measuredatetime']), np.max(data_pm100['temp'])-(range_all / 18), max_pm100_text, color = 'r', bbox = props, ha = 'left')


plt.hlines(mean_pm10, np.min(data_pm10['measuredatetime']), np.max(data_pm10['measuredatetime']), linestyle = ':', color = 'y')
plt.hlines(mean_pm25, np.min(data_pm25['measuredatetime']), np.max(data_pm25['measuredatetime']), linestyle = ':', color = 'c')
plt.hlines(mean_pm100, np.min(data_pm100['measuredatetime']), np.max(data_pm100['measuredatetime']), linestyle = ':', color = 'r')
#plt.axhline(0, color = 'k', linewidth = 0.5)

mean_pm10_text = 'Mw. ' + format(round(mean_pm10,1), '.1f') + ' (' + format(round(mean_pm10 - mean_pm10_b24,1), '.1f') + ')'
plt.text(np.max(data_pm10['measuredatetime']), mean_pm10+(range_all / 28), mean_pm10_text, color = 'y', bbox = props, ha = 'right')
mean_pm25_text = 'Mw. ' + format(round(mean_pm25,1), '.1f') + ' (' + format(round(mean_pm25 - mean_pm25_b24,1), '.1f') + ')'
plt.text(np.max(data_pm25['measuredatetime']), mean_pm25+(range_all / 28), mean_pm25_text, color = 'c', bbox = props, ha = 'right')
mean_pm100_text = 'Mw. ' + format(round(mean_pm100,1), '.1f') + ' (' + format(round(mean_pm100 - mean_pm100_b24,1), '.1f') + ')'
plt.text(np.max(data_pm100['measuredatetime']), mean_pm100+(range_all / 28)+(timesequ/10), mean_pm100_text, color = 'r', bbox = props, ha = 'right')

if max_pm25 > 25:
    print(max_pm25)
    plt.hlines(25, np.min(data_pm10['measuredatetime']), np.max(data_pm10['measuredatetime']),color = 'k', linewidth = 0.5)
    gw_pm25_text = 'GW PM2.5 (IG-L) '
    plt.text(np.max(data_pm25['measuredatetime']), 26, gw_pm25_text, color = 'k', bbox = props, rotation = 'vertical')

pltname = '/tmp/pm-vie'+str(timesequ)+'.png'
plt.savefig(pltname)

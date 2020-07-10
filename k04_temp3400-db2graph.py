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
        host = 'localhost'
        cred = netrc.netrc().authenticators(host)
        mdb_conn = mariadb.connect(host, cred[0], cred[2], 'meteo')

    except:
        print("I am unable to connect to mariadb database tempdb!")

    return mdb_conn

def read_db_hours(id, ti):
    df = pdrsq("SELECT measuredatetime, measure FROM measurement WHERE parameter_id = 1 AND sensor_id = %i ORDER BY measuredatetime DESC LIMIT %s;" %(id, ti), mdb_conn)
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
id = 2
data_i = read_db_hours(id, likedhours[0])
data_i_b24 = read_db_hours(id, likedhours[1])

id = 1
data_o = read_db_hours(id, likedhours[0])
data_o_b24 = read_db_hours(id, likedhours[1])

id = 3
data_w = read_db_hours(id, likedhours[0])
data_w_b24 = read_db_hours(id, likedhours[1])


#print(data_i)
#print(data_o)

#data_i_array() = np.asarray(data_i)
#export txt-files
#data_i_array.tofile('/home/dieter/data/temp-i.txt',sep=';')

## calculate min & mean
min_i = np.min(data_i['temp'])
min_o = np.min(data_o['temp'])
min_w = np.min(data_w['temp'])
min_i_b24 = np.min(data_i_b24['temp'])
min_o_b24 = np.min(data_o_b24['temp'])
min_w_b24 = np.min(data_w_b24['temp'])
mean_i = np.mean(data_i['temp'])
mean_o = np.mean(data_o['temp'])
mean_w = np.mean(data_w['temp'])
mean_i_b24 = np.mean(data_i_b24['temp'])
mean_o_b24 = np.mean(data_o_b24['temp'])
mean_w_b24 = np.mean(data_w_b24['temp'])
max_i = np.max(data_i['temp'])
max_o = np.max(data_o['temp'])
max_w = np.max(data_w['temp'])
max_i_b24 = np.max(data_i_b24['temp'])
max_o_b24 = np.max(data_i_b24['temp'])
max_w_b24 = np.max(data_i_b24['temp'])
min_all = np.min([min_i, min_o, min_w])
max_all = np.max([max_i, max_o, max_w])



range_all = max_all - min_all
range_hours = timesequ * 24
#print(range_all)
#print decimal('66.66666666666').quantize(decimal('1e-4'))

#print(mean_i)
#print("Min o: ")
#print(min_o)
#print("Min i: ")
#print(min_i)



d_fmt = mdates.DateFormatter('%d.%m.%Y')
h_fmt1 = mdates.DateFormatter('%H:%M')
h_fmt2 = mdates.DateFormatter('%H'+' h')
#print data_i
#print data_o
#min_i_txt = "Min (Innen): " + min_i + " °C"
ax = plt.gca()
data_i.plot(x='measuredatetime', y='temp', color="g", ax=ax, label='Innen')
data_o.plot(x='measuredatetime', y='temp', color="m", ax=ax, label='Aussen')
data_w.plot(x='measuredatetime', y='temp', color="b", ax=ax, label='Werkstatt')
#data_i.setlabel('Innen')


#ax.twinx()
if timesequ <= 2:
    days = mdates.DayLocator(interval = 1)
    hours = mdates.HourLocator(interval = 2*timesequ)
    titletxt = 'die letzten '+str(range_hours)+' Stunden:'
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt1)
#    ax.xaxis.set_minor_locator(days)
#    ax.xaxis.set_minor_formatter(d_fmt)
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
#    ax.xaxis.set_minor_locator(hours)
#    ax.xaxis.set_minor_formatter(h_fmt2)

plt.title(titletxt)
plt.xlabel('Zeit')
plt.ylabel('Temperatur (' + u'\N{DEGREE SIGN}' + 'C)')
ax.get_legend().remove()
props = dict(boxstyle='round', facecolor='white', edgecolor='white', alpha=0.7)
#ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3)


if min_o > 0:
    ax.set_ylim(0)

plt.hlines(np.min(data_i['temp']), np.min(data_i['measuredatetime']), np.max(data_i['measuredatetime']), linestyle = '--', color = 'g')
plt.hlines(np.max(data_i['temp']), np.min(data_i['measuredatetime']), np.max(data_i['measuredatetime']), linestyle = 'solid', color = 'g')
plt.hlines(np.min(data_o['temp']), np.min(data_o['measuredatetime']), np.max(data_o['measuredatetime']), linestyle = '--', color = 'm')
plt.hlines(np.max(data_o['temp']), np.min(data_o['measuredatetime']), np.max(data_o['measuredatetime']), linestyle = 'solid', color = 'm')
plt.hlines(np.min(data_w['temp']), np.min(data_w['measuredatetime']), np.max(data_w['measuredatetime']), linestyle = '--', color = 'b')
plt.hlines(np.max(data_w['temp']), np.min(data_w['measuredatetime']), np.max(data_w['measuredatetime']), linestyle = 'solid', color = 'b')
plt.hlines(mean_i, np.min(data_i['measuredatetime']), np.max(data_i['measuredatetime']), linestyle = ':', color = 'g')
plt.hlines(mean_o, np.min(data_o['measuredatetime']), np.max(data_o['measuredatetime']), linestyle = ':', color = 'm')
plt.hlines(mean_w, np.min(data_w['measuredatetime']), np.max(data_w['measuredatetime']), linestyle = ':', color = 'b')


min_i_text = 'Min. ' + format(round(min_i,1), '.1f') + ' (' + format(round(min_i - min_i_b24,1), '.1f') + ')'
max_i_text = 'Max. ' + format(round(max_i,1), '.1f') + ' (' + format(round(max_i - max_i_b24,1), '.1f') + ')'
mean_i_text = 'Mw. ' + format(round(mean_i,1), '.1f') + ' (' + format(round(mean_i - mean_i_b24,1), '.1f') + ')'
plt.text(np.min(data_i['measuredatetime']), np.min(data_i['temp'])-(range_all / 18), min_i_text, color = 'g', bbox = props)
plt.text(np.min(data_i['measuredatetime']), np.max(data_i['temp'])+(range_all / 18), max_i_text, color = 'g', bbox = props)
plt.text(np.max(data_i['measuredatetime']), mean_i+(range_all / 28), mean_i_text, color = 'g', bbox = props, ha = 'right')


min_o_text = 'Min. ' + format(round(min_o,1), '.1f') + ' (' + format(round(min_o - min_o_b24,1), '.1f') + ')'
max_o_text = 'Max. ' + format(round(max_o,1), '.1f') + ' (' + format(round(max_o - max_o_b24,1), '.1f') + ')'
mean_o_text = 'Mw. ' + format(round(mean_o,1), '.1f') + ' (' + format(round(mean_o - mean_o_b24,1), '.1f') + ')'
plt.text(np.min(data_o['measuredatetime']), np.min(data_o['temp'])-(range_all / 18), min_o_text, color = 'm', bbox = props, ha = 'left')
plt.text(np.min(data_o['measuredatetime']), np.max(data_o['temp'])+(range_all / 18), max_o_text, color = 'm', bbox = props, ha = 'left')
plt.text(np.max(data_o['measuredatetime']), mean_o+(range_all / 28), mean_o_text, color = 'm', bbox = props, ha = 'right')

min_w_text = 'Min. ' + format(round(min_w,1), '.1f') + ' (' + format(round(min_w - min_w_b24,1), '.1f') + ')'
max_w_text = 'Max. ' + format(round(max_w,1), '.1f') + ' (' + format(round(max_w - max_w_b24,1), '.1f') + ')'
mean_w_text = 'Mw. ' + format(round(mean_w,1), '.1f') + ' (' + format(round(mean_w - mean_w_b24,1), '.1f') + ')'
plt.text(np.min(data_w['measuredatetime']), np.min(data_w['temp'])-(range_all / 18), min_w_text, color = 'b', bbox = props, ha = 'left')
plt.text(np.min(data_w['measuredatetime']), np.max(data_w['temp'])+(range_all / 18), max_w_text, color = 'b', bbox = props, ha = 'left')
plt.text(np.max(data_w['measuredatetime']), mean_w+(range_all / 28)+(timesequ/10), mean_w_text, color = 'b', bbox = props, ha = 'right')


#plt.axhline(0, color = 'k', linewidth = 0.5)
#plt.text(np.min(data_w['measuredatetime']), mean_w+(range_all / 28)+(timesequ/10), "GitTest", color = 'k', bbox = props, ha = 'right')


pltname = '/tmp/temp'+str(timesequ)+'.png'
plt.savefig(pltname)

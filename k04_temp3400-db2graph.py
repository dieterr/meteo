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
import datetime
from dateutil.relativedelta import relativedelta
import requests, json

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
        engine = create_engine(url_object)

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


class getDataFromGrid():

    def __init__(self, parameters, start, end, bbox):
        self.gridParams = dict(
            parameters=parameters,
            start=start,
            end=end,
            bbox=bbox
        )
        self.url = "https://dataset.api.hub.geosphere.at/v1/grid/historical/inca-v1-1h-1km"
        try:
            resp = requests.get(url=self.url, params=self.gridParams)
            resp.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            self.rawData = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching grid data: {e}")
            self.rawData = None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for grid data: {e}")
            self.rawData = None


class GeosphereData:
    def __init__(self, name, raw_data):
        self.name = name
        self.raw_data = raw_data

    def __repr__(self):
        return f"GeosphereData(name={self.name}, raw_data={self.raw_data})"

class CorrelationCalculator:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def calculate_pearson(self):
        # Ensure both dataframes have the same time index
        merged_df = pd.merge(self.df1, self.df2, left_on='measuredatetime', right_on='time', suffixes=('_out', '_klosterneuburg'))
        if merged_df.empty:
            print("No overlapping data to calculate correlation.")
            return None
        correlation = merged_df['temp_out'].corr(merged_df['temp_klosterneuburg'], method='pearson')
        return correlation

# Main script

print('Number of arguments:', len(sys.argv), 'arguments.')

timeSequ = int(sys.argv[2])


local_timezone = datetime.datetime.now().astimezone().tzinfo
print(f"Local timezone info: {local_timezone}")

localStartDateTime = datetime.datetime.strptime(str(datetime.datetime.now() - relativedelta(days=timeSequ)),"%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=local_timezone).strftime("%Y-%m-%dT%H:%M")
localEndDateTime = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=local_timezone).strftime("%Y-%m-%dT%H:%M")
utcStartDateTime = datetime.datetime.strptime(localStartDateTime, "%Y-%m-%dT%H:%M").replace(tzinfo=local_timezone).astimezone(datetime.timezone.utc)
utcEndDateTime = datetime.datetime.strptime(localEndDateTime, "%Y-%m-%dT%H:%M").replace(tzinfo=local_timezone).astimezone(datetime.timezone.utc)

likedHours1Begin = timeSequ * 24
likedHours1End = 0 
likedHours2Begin = timeSequ * 24 * 2
likedHours2End = timeSequ * 24

engine = db_connect()

data_all = read_db_all(likedHours1Begin, likedHours1End)

geosphere_objects = []

favoritePoints = [
    {"name": "Klosterneuburg Laube", "lat": 48.31, "lon": 16.32},
    {"name": "Wien", "lat": 48.19, "lon": 16.31}]

parameters = "T2M"

for point in favoritePoints:
    bbox = f"{point['lat']-0.01},{point['lon']-0.01},{point['lat']+0.01},{point['lon']+0.01}"  # Create a small bounding box around the point

    grid_data = getDataFromGrid(parameters, utcStartDateTime, utcEndDateTime, bbox)
    if grid_data.rawData:
        geosphere_object = GeosphereData(point['name'], grid_data.rawData)
        geosphere_objects.append(geosphere_object)
    else:
        print(f"Failed to fetch data for {point['name']}")

geosphere_dataframes = {}

for obj in geosphere_objects:
    if obj.raw_data and 'features' in obj.raw_data:
        features = obj.raw_data['features']
        if features and 'properties' in features[0] and 'parameters' in features[0]['properties']:
            temp_data = features[0]['properties']['parameters']['T2M']['data']
            timestamps = obj.raw_data['timestamps']
            timestamps = list(map(lambda c: (datetime.datetime.strptime(c, "%Y-%m-%dT%H:%M+%S:%f") + datetime.timedelta(hours=local_timezone.utcoffset(None).total_seconds() / 3600)), timestamps))
            geosphere_dataframes[obj.name] = pd.DataFrame({'time': timestamps, 'temp': temp_data})
        else:
            print(f"No valid data found for {obj.name}")
    else:
        print(f"No valid data found for {obj.name}")


likedHours1Begin = timeSequ * 24
likedHours1End = 0 
likedHours2Begin = timeSequ * 24 * 2
likedHours2End = timeSequ * 24

engine = db_connect()

data_all = read_db_all(likedHours1Begin, likedHours1End)

stat = statistics(data_all)

stat = statistics(data_all)

min_all = stat[0]
max_all = stat[1]

range_all = max_all - min_all

sensorList = {"out":[1,"m"],"in":[2,"g"],"workshop":[3,"b"]}

axt = plt.gca()

props = dict(boxstyle='round', facecolor='white', edgecolor='white', alpha=0.7)

for i in sensorList:
    data_now = read_db_hours(sensorList[i][0], likedHours1Begin, likedHours1End)
    data_old = read_db_hours(sensorList[i][0], likedHours2Begin, likedHours2End)
    if data_now.empty or data_old.empty:
        next
    else:
        draw_tempData(data_now,data_old)

    draw_tempData(data_now,data_old)
    
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



if geosphere_dataframes['Klosterneuburg Laube'].empty == True:
    pass
else:
    geosphere_dataframes['Klosterneuburg Laube'].plot(x='time', y='temp', color='black', ax=axt, label='GeoSphere INCA hourly', linewidth=1.5)


plt.title(titletxt)
plt.xlabel('Zeit')
plt.ylabel('Temperatur (' + u'\N{DEGREE SIGN}' + 'C)')

axt.get_legend().remove()

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=4)

if min_all > 0:
    axt.set_ylim(0)

plt.axhline(0, color = 'k', linewidth = 0.5)

# Example usage
if 'out' in sensorList and 'Klosterneuburg Laube' in geosphere_dataframes:
    out_data = read_db_hours(sensorList["out"][0], likedHours1Begin, likedHours1End)
    klosterneuburg_data = geosphere_dataframes['Klosterneuburg Laube']
    if not out_data.empty and not klosterneuburg_data.empty:
        correlation_calculator = CorrelationCalculator(out_data, klosterneuburg_data)
        pearson_correlation = correlation_calculator.calculate_pearson()
        if pearson_correlation is not None:
            print(f"Pearson correlation between 'out' and 'Klosterneuburg Laube': {pearson_correlation}")

pltname = '/home/dieter/temp'+str(timeSequ)+'.png'
plt.savefig(pltname)
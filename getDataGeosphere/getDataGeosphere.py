#!/usr/bin/python                                                                                                    
# -*- coding: utf-8 -*-

import requests,json
import pandas as pd



stations = [
    # {"id": 4070, "name": "Korneuburg"},
    # {"id": 4071, "name": "Korneuburg"},
    {"id": 4115, "name": "Wien/Stammersdorf"}
    # {"id": 4112, "name": "Wien-Kahlenberg"},
    # {"id": 4030, "name": "Stockerau"},
    # {"id": 4081, "name": "Langenlebarn"},
    # {"id": 4080, "name": "Langenlebarn"}
]

favoritePoints = [
    {"name": "Klosterneuburg Laube", "lat": 48.31, "lon": 16.32},
    {"name": "Wien", "lat": 48.19, "lon": 16.31}]

# url = "https://dataset.api.hub.geosphere.at/v1/station/historical/"
url = "https://dataset.api.hub.geosphere.at/v1/grid/historical/inca-v1-1h-1km"
parameters = "T2M"
start = "2023-04-19T00:00" #"2025-04-19T00:00"
end = "2023-04-26T23:50" #"2025-04-26T23:50"
# bbox = "48.31,16.32,48.32,16.33" 

class getDataFromGrid():
    def __init__(self, parameters, start, end, bbox):
        self.gridParams = dict(
            parameters=parameters,
            start=start,
            end=end,
            bbox=bbox
        )
        try:
            resp = requests.get(url=url, params=self.gridParams)
            resp.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            self.rawData = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching grid data: {e}")
            self.rawData = None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for grid data: {e}")
            self.rawData = None


for point in favoritePoints:
    bbox = f"{point['lat']-0.01},{point['lon']-0.01},{point['lat']+0.01},{point['lon']+0.01}"  # Create a small bounding box around the point
    grid_data = getDataFromGrid(parameters, start, end, bbox)
    if grid_data.rawData:
        print(f"Data for {point['name']}:")
        print(json.dumps(grid_data.rawData, indent=2))  # Pretty-print the JSON data
    else:
        print(f"Failed to fetch data for {point['name']}")

class getDataFromStation():
    def __init__(self, parameters, start, end, station_id):
        self.stationParams = dict(
            parameters=parameters,
            start=start,
            end=end,
            bbox=bbox
            )
        try:
            resp = requests.get(url=url, params=self.stationParams)
            resp.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            self.rawData = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for station {station_id}: {e}")
            self.rawData = None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for station {station_id}: {e}")
            self.rawData = None
    

#print(rawData)

# station_objects = []
# for station in stations:
#     station_object = getDataFromStation(parameters, start, end, bbox)
#     station_objects.append(station_object)

# station_object = getDataFromStation(parameters, start, end, bbox)    
# print(station_object.rawData)


# time = rawData['timestamps']
# temp = rawData['features'][0]['properties']['parameters']['TL']['data']

# df = pd.DataFrame(temp,index=time,columns=['4115'])
# df2 = pd.DataFrame(data={'time':time,'temp':temp})

# print(df)
# print(df2)
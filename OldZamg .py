# parametersZamg = dict(
#     parameters="T2M",
#     start=actualstartDateTime,
#     end=actualEndDateTime,
#     station_ids=4115
#     )
#     #4070 Korneuburg; 4071 Korneuburg; 4115 Wien/Stammersdorf; 4112 Wien-Kahlenberg
#     #4030 Stockerau; 4081 Langenlebarn; 4080 Langenlebarn

# zamgData = read_zamgData(parametersZamg)

# indexData = zamgData['time']
# zamgDataHistory = pd.DataFrame(data=indexData)

# for i in range(1,20):
#     # print(i)
#     actualYear = datetime.datetime.strptime(str(datetime.datetime.now() - relativedelta(years=i)),"%Y-%m-%d %H:%M:%S.%f").strftime("%Y")
#     #print(actualYear)
#     startDateTime = datetime.datetime.strptime(str(datetime.datetime.now() - relativedelta(years=i) - relativedelta(days=timeSequ)),"%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%dT%H:%M")
#     # print(startDateTime)
#     endDateTime = datetime.datetime.strptime(str(datetime.datetime.now() - relativedelta(years=i)),"%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%dT%H:%M")
#     print(endDateTime)

#     parametersZamg["start"] = startDateTime
#     parametersZamg["end"] = endDateTime


#     if i == 0:
#         zamgData = read_zamgData(parametersZamg)
#     else:
#         zamgDataRead = read_zamgData(parametersZamg)
#         zamgDataHistory[actualYear] = zamgDataRead['temp']

# # print("fresh",zamgData)
# print("old",zamgDataHistory)

#     # print(parametersZamg["start"])

# zamgDataHistory['stdDev'] = zamgDataHistory.std(axis=1)
# zamgDataHistory['avg'] = zamgDataHistory.mean(axis=1,numeric_only=True)

# zamgDataHistory['low'] = zamgDataHistory['avg'] - zamgDataHistory['stdDev']
# zamgDataHistory['high'] = zamgDataHistory['avg'] + zamgDataHistory['stdDev']



# print(zamgDataHistory['stdDev'])
# print(zamgDataHistory['avg'])
# print(zamgDataHistory['low'])
# print(zamgDataHistory['high'])



#print('timesequ: ', timeSequ)


#print(titletxt)

#print(dfZamg)

# stddev = zamgDataHistory['stdAbw']
# print("stddev",stddev)
# y1 = zamgDataHistory['stdAbw']-stddev
# y2 = zamgDataHistory['stdAbw']+stddev
# print("y1",y1,"y2",y2)



# if zamgData.empty == True:
#     pass
# else:
#     zamgData.plot(x='time', y='temp', color='r', ax=axt, label='refStation',linewidth=0.5)

# zamgDataHistory.plot(x='time',y='avg',color='r',ax=axt, label='refStation')
# plt.fill_between(x='time',y1='low',y2='high',alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')

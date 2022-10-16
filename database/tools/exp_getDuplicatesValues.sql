SELECT sensor_id,
       parameter_id,
       measuredatetime,
       measure,
       isDeleted,
       COUNT(id) AS cnt
INTO OUTFILE '/tmp/duplicates202201032324.csv'
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM measurement
GROUP BY sensor_id, parameter_id, measuredatetime, measure, isDeleted
HAVING cnt > 1;

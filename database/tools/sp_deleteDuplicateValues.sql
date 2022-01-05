DELIMITER //

CREATE OR REPLACE PROCEDURE meteo.sp_removeDuplicates()

BEGIN

CREATE TEMPORARY TABLE basicL
       (id int,
       sensorId int,
       paramterId int,
       measuredatetime datetime
       );

INSERT INTO basicL
SELECT me.id,
       me.sensor_id,
       me.parameter_id,
       me.measuredatetime
/*
INTO OUTFILE '/tmp/duplicatesIds202201032352.csv'
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
*/
FROM measurement AS me
INNER JOIN (SELECT sensor_id,
       parameter_id,
       measuredatetime,
       measure,
       isDeleted
       FROM measurement
       GROUP BY sensor_id, parameter_id, measuredatetime, measure, isDeleted
       HAVING COUNT(id) > 1) AS dup
       ON me.sensor_id = dup.sensor_id
       AND me.parameter_id = dup.parameter_id
       AND me.measuredatetime = dup.measuredatetime
       AND me.measure = dup.measure
       AND me.isDeleted = dup.isDeleted
WHERE me.isDeleted = 0
      AND me.measuredatetime >= '2020-03-30 20:00'
ORDER BY me.sensor_id,
       me.parameter_id,
       me.measuredatetime,
       me.measure,
       me.isDeleted;


SELECT *
FROM basicL;

DROP TABLE basicL;

END

//

DELIMITER ;

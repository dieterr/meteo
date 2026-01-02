/*
CALL meteo.sp_getTimeseries('2024-01-01','2024-02-01',0,'10-000802a8876f')
*/



CREATE OR REPLACE PROCEDURE meteo.sp_getTimeseries (
	IN startDate DATE
	,IN endDate DATE
	,IN ytd BIT
	,IN sensorName TINYTEXT)

BEGIN

IF (ytd = 1) THEN
	SET startDate = IFNULL(MAKEDATE(YEAR (NOW()),1),startDate);
END IF;

SET endDate = IFNULL(endDate,NOW());

SELECT DISTINCT me.measuredatetime,
       se.name AS sensorName,
       pa.name AS parameterName,
       me.measure
FROM measurement AS me
INNER JOIN parameter pa ON
me.parameter_id = pa.id
INNER JOIN sensor se ON
me.sensor_id = se.id 
WHERE me.isDeleted = 0
      AND pa.id = 1
      AND se.name = sensorName
      AND me.measuredatetime >= startDate      
      AND me.measuredatetime <= endDate
ORDER BY me.sensor_id,
       me.parameter_id,
       me.measuredatetime,
       me.measure;

END;

-- //

-- DELIMITER ;

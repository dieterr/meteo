-- DELIMITER //


-- { CALL meteo.sp_getTimeseries(:startDate,:endDate,:sensorName) }




CREATE OR REPLACE PROCEDURE meteo.sp_getTimeseries (
	IN startDate DATE
	,IN endDate DATE
	-- ,IN ytd BIT
	,IN sensorName TINYTEXT)

BEGIN

-- IF ytd = 1
-- BEGIN 
	SET startDate = MAKEDATE(YEAR (NOW()),1);
	
-- END

	
SET endDate = IFNULL(NOW(),endDate);

SELECT me.measuredatetime,
       se.name,
       pa.name,
       me.measure
       
FROM measurement AS me

INNER JOIN parameter pa ON
me.parameter_id = pa.id

INNER JOIN sensor se ON
me.sensor_id = se.id 

-- WHERE me.isDeleted = 0
      -- AND me.measuredatetime >= startDate      
      -- AND me.measuredatetime <= endDate
ORDER BY me.sensor_id,
       me.parameter_id,
       me.measuredatetime,
       me.measure;

END;

-- //

-- DELIMITER ;

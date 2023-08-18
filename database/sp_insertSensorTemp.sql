/* CALL meteo.insertTempDatscha(
	'10-000802a827d4',
	1,
	'2022-10-14 04:15:05',
	0) */


DELIMITER //

CREATE OR REPLACE PROCEDURE insertTempDatscha(
	IN sensorNameIn VARCHAR(50),
	IN parameterIDIn SMALLINT,
	IN measuredatetimeIn DATETIME,
  	IN toUpdate BIT -- DEFAULT = 0
  	)

BEGIN

DECLARE sensorID SMALLINT;

SET toUpdate = 0;

SELECT sensorNameIn;

SELECT se.id
INTO sensorID
FROM sensor AS se
WHERE se.name = sensorNameIn;

SELECT sensorId;

SELECT me.id
	,me.measuredatetime 
FROM measurement AS me
WHERE me.sensor_id = sensorID
      AND me.parameter_id = parameterIDIn
      AND DATE(me.measuredatetime) = DATE(measuredatetimeIn)
      AND HOUR(me.measuredatetime) = MINUTE(measuredatetimeIn)
      AND MINUTE(me.measuredatetime) = MINUTE(measuredatetimeIn);


SELECT IF (
(SELECT me.id
FROM measurement AS me
WHERE me.sensor_id = sensorID
      AND me.parameter_id = parameterIDIn
      AND me.measuredatetime = measuredatetimeIn) IS NULL , 'ok', 'nok');


     
      #AND HOUR(me.measuredatetime) = MINUTE(measuredatetimeIn)
      #AND MINUTE(me.measuredatetime) = MINUTE(measuredatetimeIn)
     
      # THEN SELECT 'got it!'

      # END IF;

# BEGIN
#	SELECT 'test';
# END;
      
END;

//

DELIMITER ;
DELIMITER //

CREATE OR REPLACE PROCEDURE meteo.sp_insertTempRecords(
  sensornameIn VARCHAR(50),
  measuredatetimeIn DATETIME,
  parameteridIn SMALLINT(5),
  measureIn DECIMAL(4,1)
  )
BEGIN

	DECLARE sensorId SMALLINT;

	SET sensorId = meteo.fn_getSensorid(sensornameIn);
	
	SELECT sensorId;
	
	INSERT INTO measurement
	(sensor_id, parameter_id, measuredatetime, measure)
	SELECT sensorId,parameteridIn,measuredatetimeIn,measureIn
	FROM DUAL
	WHERE NOT EXISTS (SELECT *
	      FROM measurement
	      WHERE sensor_id = sensorId
	      AND measuredatetime = measuredatetimeIn
	      AND measure = measureIn
	      AND parameter_id = parameteridIn);

END

/*
SELECT se.id
INTO @sensorId
FROM sensor AS se
WHERE se.name = sensornameIn;

SELECT @sensorId;
*/
/*
SELECT IF((
SELECT me.id
FROM measurement AS me
WHERE me.sensor_id = @sensorId
      AND me.parameter_id = parameteridIn
      AND me.measuredatetime = measuredatetimeIn;)=NULL
      ,'test','bla');

BEGIN
	SELECT 'test'
END
*/
//

DELIMITER ;

/*
select routine_schema as meteodb,
       routine_name,
       routine_type as type,
       data_type as return_type,
       routine_definition as definition
from information_schema.routines
where routine_schema not in ('sys', 'information_schema',
       'mysql', 'performance_schema')
       -- and r.routine_schema = 'database_name' -- put your database name here
order by routine_schema, routine_name;
*/

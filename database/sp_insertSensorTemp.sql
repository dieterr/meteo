-- DELIMITER //
DROP PROCEDURE insertTempDatscha;

CREATE PROCEDURE insertTempDatscha(
sensornameIn VARCHAR(50),
measuredatetimeIn DATETIME,
parameteridIn SMALLINT(5),
measureIn DECIMAL(4,1)
)
BEGIN

SET @sensorId = 'test';
SET @toUpdate = 0;

SELECT @sensorId;

SELECT se.id
INTO @sensorId
FROM sensor AS se
WHERE se.name = sensornameIn;

SELECT @sensorId;

-- SELECT IF((
-- SELECT me.id
-- FROM measurement AS me
-- WHERE me.sensor_id = @sensorId
--       AND me.parameter_id = parameteridIn
--       AND me.measuredatetime = measuredatetimeIn;)=NULL
--       ,'test','bla');

-- BEGIN
-- 	SELECT 'test'
END;

-- //

-- DELIMITER ;



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

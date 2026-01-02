CREATE OR REPLACE PROCEDURE meteo.insertTempDatscha
       (SensornameIn TINYTEXT,
        ParameteridIn INT,
        MeasuredatetimeIn DATETIME,
        ValueIn FLOAT)

/*
Programmers comment:
Insert temperature measurement from sensors

example call:
CALL insertTempDatscha('10-000802a827d4', 1, '2017-04-22 17:30:03', 23.5);
-- CALL insertTempDatscha('10-000802a8876f,', 1, '17-04-22', 23.5);
*/

BEGIN

DECLARE SensorId INT;

SELECT se.id
INTO SensorId
FROM sensor AS se
WHERE se.name = @SensornameIn COLLATE utf8mb4_general_ci;


IF EXISTS(SELECT me.id
           FROM measurement AS me
           WHERE me.sensor_id = SensorId
                 AND me.parameter_id = ParameteridIn
                 AND me.measuredatetime = MeasuredatetimeIn) THEN

    -- entry already exists, do nothing
    SELECT 'entry already exists' AS result;

ELSE

    -- insert new measurement
    INSERT INTO measurement (sensor_id,
                             parameter_id,
                             measure,
                             measuredatetime,
                             isDeleted)
    VALUES (SensorId,
            ParameteridIn,
            ValueIn,
            MeasuredatetimeIn,
            0);

    SELECT 'new entry inserted' AS result;

END IF;

-- SELECT me.id,
--        me.sensor_id,
--        me.parameter_id,
--        me.measure,
--        me.measuredatetime,
--        me.isDeleted
-- FROM measurement AS me
-- WHERE me.sensor_id = SensorId
--       AND me.parameter_id = ParameteridIn
--       AND me.measuredatetime = MeasuredatetimeIn;

-- SELECT IF((
-- SELECT me.id,
--        me.sensor_id,
--        me.parameter_id,
--        me.measure,
--        me.measuredatetime,
--        me.isDeleted
-- FROM measurement AS me
-- WHERE me.sensor_id = SensorId
--       AND me.parameter_id = ParameteridIn
-- --       AND CAST(me.measuredatetime AS DATE) = MeasuredatetimeIn;
--       AND me.measuredatetime = MeasuredatetimeIn)
--       , 'no entry', 'entry') AS result;


-- SELECT IF((
-- SELECT me.id
-- FROM measurement AS me
-- WHERE me.sensor_id = SensorId
--       AND me.parameter_id = ParameteridIn
--       AND me.measuredatetime = MeasuredatetimeIn)=NULL
--       ,'test','bla');

-- BEGIN
-- 	SELECT 'test'
END;



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

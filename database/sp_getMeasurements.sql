CREATE OR REPLACE PROCEDURE meteo.getMeasurements
       (MeasuredatetimeFrom DATETIME)

/*
Programmers comment:
Insert temperature measurement from sensors

example call:
CALL meteo.getMeasurements('2024-04-22 17:30:03');
-- CALL meteo.getMeasurements('17-04-22');
*/

BEGIN


SELECT se.name,
    me.measuredatetime,
    me.measure
FROM measurement AS me
INNER JOIN meteo.sensor AS se ON
me.sensor_id = se.id
WHERE me.measuredatetime >= MeasuredatetimeFrom
    AND me.parameter_id = 1
ORDER BY me.measuredatetime, me.sensor_id;


END;



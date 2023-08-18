CREATE OR REPLACE FUNCTION fn_getSensorId (sensorName TINYTEXT) RETURNS INT RETURN   (SELECT id FROM sensor WHERE sensor.name = sensorName);

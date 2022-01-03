DELIMITER //

CREATE OR REPLACE FUNCTION meteo.fn_getSensorId(sensorName TINYTEXT)
RETURNS INT
BEGIN
RETURN   (SELECT id
	 FROM sensor
	 WHERE sensor.name = sensorName);
END

//

DELIMITER ;

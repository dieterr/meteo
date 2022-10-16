DELIMITER //

CREATE OR REPLACE PROCEDURE meteo.sp_removeDuplicates()

BEGIN

DECLARE done INT DEFAULT FALSE;
DECLARE x INT;
DECLARE cur CURSOR FOR SELECT idid FROM basicL;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

CREATE TEMPORARY TABLE basicL
       (idid int NOT NULL AUTO_INCREMENT,
       id int,
       sensorId int,
       paramterId int,
       measuredatetime datetime,
       measure decimal(4,2),
       PRIMARY KEY (idid)
       );

CREATE TEMPORARY TABLE resultL
       (rid int NOT NULL AUTO_INCREMENT,
       idid int NOT NULL,
       PRIMARY KEY (rid)
       );


INSERT INTO basicL
SELECT 0,
       me.id,
       me.sensor_id,
       me.parameter_id,
       me.measuredatetime,
       me.measure
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

OPEN cur;

read_loop: LOOP
	   FETCH cur INTO x;
	   IF done THEN
	      LEAVE read_loop;
	   END IF;

	   IF x % 2 = 0 THEN
	      INSERT INTO resultL VALUES (0,x);
	   ELSE
	      INSERT INTO resultL VALUES (0,1);
	   END IF;

END LOOP;

CLOSE cur;

SELECT *
FROM basicL;

SELECT resultL.*, basicL.*
FROM resultL
LEFT JOIN basicL ON resultL.rid = basicL.idid;

DROP TABLE basicL;
DROP TABLE resultL;

END

//

DELIMITER ;

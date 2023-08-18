-- DECLARE city VARCHAR(30);

-- SELECT @city;

-- SHOW VARIABLES;

-- SET city = 'New York';


SELECT YEAR(m.measuredatetime)
	,MONTH(m.measuredatetime)
	,DAY(m.measuredatetime)
	,ROUND(AVG(m.measure),2)
FROM measurement m 
WHERE m.parameter_id = 1
	AND m.sensor_id = 1
	AND m.isDeleted = 0
	AND m.measuredatetime BETWEEN '2022-03-01' AND NOW()
GROUP BY DAY(m.measuredatetime), MONTH(m.measuredatetime), YEAR(m.measuredatetime)
ORDER BY measuredatetime;

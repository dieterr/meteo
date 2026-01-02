SELECT S.place,
	M.measuredatetime,
	M.measure
FROM measurement AS M
INNER JOIN sensor AS S ON
M.sensor_id = S.id
WHERE M.parameter_id = 1
	AND M.isDeleted = 0
	AND M.measuredatetime > DATE_ADD(NOW(), INTERVAL -48 HOUR)
ORDER BY M.measuredatetime;

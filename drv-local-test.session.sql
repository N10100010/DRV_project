

select count(
    distinct race_boat_id
) from intermediate_times




SELECT boat_classes.id, boat_classes.additional_id_, boat_classes.abbreviation, boat_classes.name, boat_classes.world_best_race_boat_id 
FROM boat_classes JOIN race_boats ON race_boats.id = boat_classes.world_best_race_boat_id


SELECT boat_classes.id, boat_classes.additional_id_, boat_classes.abbreviation, boat_classes.name, boat_classes.world_best_race_boat_id 
FROM boat_classes JOIN race_boats ON race_boats.id = boat_classes.world_best_race_boat_id 
WHERE boat_classes.id = :id_1

select *
from boat_classes



update intermediate_times
set is_outlier = NULL


UPDATE 
    intermediate_times 
SET is_outlier=TRUE
WHERE 
    intermediate_times.race_boat_id = 120


select count(*)
from intermediate_times
where is_outlier = TRUE


select count(*)
from intermediate_times
join ()
group by 

select * 
form intermediate_times
where boat



UPDATE 
    intermediate_times 
SET is_outlier= 
WHERE 
    intermediate_times.race_boat_id = :race_boat_id_1 
    AND intermediate_times.distance_meter = :distance_meter_1
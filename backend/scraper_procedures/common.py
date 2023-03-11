from model import model
# from model import dbutils

def bubble_up_2km_intermediate(intermediate: model.Intermediate_Time):
    """ writes 2km intermediate data to Race_Boat entity
    """
    if not intermediate.distance_meter == 2000:
        raise ValueError("Not a 2km intermediate entity")
    
    intermediate.race_boat.result_time_ms = intermediate.result_time_ms
    intermediate.race_boat.invalid_mark_result_code_id = intermediate.invalid_mark_result_code_id
    intermediate.race_boat.rank = intermediate.rank

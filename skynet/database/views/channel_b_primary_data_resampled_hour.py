channel_b_primary_data_resampled_hour = """
create or replace view channel_b_primary_data_resampled_hour as (select instrument_id as instrument_id_b, 
																   date_trunc('hour', time) as time_by_hour_b, 
																   round(avg(pm1_atm), 3) as pm1_atm_b, 
																   round(avg(pm25_atm), 3) as pm25_atm_b,
																   round(avg(pm10_atm), 3) as pm10_atm_b,
																   round(avg(pressure), 3) as pressure,
																   round(avg(pm25_cf_1), 3) as pm25_cf_1_b
															from channel_b_primary_data 
															group by 1, time_by_hour_b, latitude 
															order by time_by_hour_b asc);
"""
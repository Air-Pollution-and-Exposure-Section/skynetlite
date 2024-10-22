channel_a_primary_data_resampled_minute = """
create or replace view channel_a_primary_data_resampled_minute as (select instrument_id as instrument_id_a, 
																   date_trunc('minute', time) as time_by_minute_a, 
																   latitude,
																   longitude, 
																   device_location_type,
																   round(avg(pm1_atm), 3) as pm1_atm_a, 
																   round(avg(pm25_atm), 3) as pm25_atm_a,
																   round(avg(pm10_atm), 3) as pm10_atm_a,
																   round(avg(uptime), 3) as uptime,
																   round(avg(temperature), 3) as temperature,
																   round(avg(humidity), 3) as humidity,
																   round(avg(dew_point), 3) as dew_point,
																   round(avg(pm25_cf_1), 3) as pm25_cf_1_a
															from channel_a_primary_data 
															group by 1, time_by_minute_a, latitude, longitude, device_location_type 
															order by time_by_minute_a asc);
"""
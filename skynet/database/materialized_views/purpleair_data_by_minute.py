purpleair_data_by_minute = """
create materialized view purpleair_data_by_minute as (select distinct instrument_id_a as instrument_id,
															time_by_minute_a as time,
														    latitude as latitude,
														    longitude as longitude,
														    channel_a_primary_data_resampled_minute.device_location_type as location_type,
														    temperature as temperature,
											                humidity as humidity,
											                round(get_average(pm1_atm_a, pm1_atm_b), 2) as pm1cf1,
											               	round(get_pm25_corrected(pm25_atm_a, pm25_atm_b), 2) as pm25cf1,
											               	round(get_average(pm10_atm_a, pm10_atm_b), 2) as pm10cf1,
											               	round(get_average(pm25_cf_1_a, pm25_cf_1_b), 2) as pm25atm,
											               	round(get_pm25_epa(get_pm25_corrected(pm25_atm_a, pm25_atm_b), channel_a_primary_data_resampled_minute.humidity), 2) as pm25_EPA,
															round(get_pm25_unbc(get_pm25_corrected(pm25_atm_a, pm25_atm_b), channel_a_primary_data_resampled_minute.humidity), 2) as pm25_UNBC,
											                study.name as study_name
											from channel_a_primary_data_resampled_minute
											inner join channel_b_primary_data_resampled_minute
											on channel_a_primary_data_resampled_minute.time_by_minute_a=channel_b_primary_data_resampled_minute.time_by_minute_b
											and channel_a_primary_data_resampled_minute.instrument_id_a=channel_b_primary_data_resampled_minute.instrument_id_b
											inner join channel_a_secondary_data_resampled_minute
											on channel_a_primary_data_resampled_minute.time_by_minute_a=channel_a_secondary_data_resampled_minute.time_by_minute_c
											and channel_a_primary_data_resampled_minute.instrument_id_a=channel_a_secondary_data_resampled_minute.instrument_id_c
											inner join channel_b_secondary_data_resampled_minute
											on channel_a_primary_data_resampled_minute.time_by_minute_a=channel_b_secondary_data_resampled_minute.time_by_minute_d
											and channel_a_primary_data_resampled_minute.instrument_id_a=channel_b_secondary_data_resampled_minute.instrument_id_d
											 full outer join responsibility on channel_a_primary_data_resampled_minute.instrument_id_a=responsibility.instrument_id 
											 full outer join participation on responsibility.participant_id=participation.participant_id
											 full outer join study on participation.study_id=study.id
											where channel_a_primary_data_resampled_minute.instrument_id_a is not null
											and round(get_pm25_corrected(pm25_atm_a, pm25_atm_b), 2) is not NULL
											order by instrument_id, time asc);
"""
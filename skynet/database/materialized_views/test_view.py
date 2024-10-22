test_view = """
create materialized view test_view as (select distinct instrument_id_a as instrument_id,
														time_by_minute_a as time,
													    latitude as latitude,
													    longitude as longitude,
													    temperature as temperature,
										                humidity as humidity,
										                pm1_atm_a as pm1cf1_a,
										                pm1_atm_b as pm1cf1_b,
										                pm25_atm_a as pm25cf1_a,
										                pm25_atm_b as pm25cf1_b,
										                pm10_atm_a as pm10cf1_a,
										                pm10_atm_b as pm10cf1_b,
										                pm25_cf_1_a as pm25_atm_a,
										                pm25_cf_1_b as pm25_atm_b
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
											order by instrument_id, time asc);
"""
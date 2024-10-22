channel_a_secondary_data_resampled_hour = """
create or replace view channel_a_secondary_data_resampled_hour as (select instrument_id as instrument_id_c,
																	 date_trunc('hour', time) as time_by_hour_c,
																	 round(avg(um3), 3) as um3_a,
																	 round(avg(um5), 3) as um5_a,
																	 round(avg(um1), 3) as um1_a,
																	 round(avg(um25), 3) as um25_a,
																	 round(avg(um50), 3) as um50_a,
																	 round(avg(um10), 3) as um10_a,
																	 round(avg(pm1_cf_1), 3) as pm1_cf_1_a,
																	 round(avg(pm10_cf_1), 3) as pm10_cf_1_a
															 from channel_a_secondary_data
															 group by 1, time_by_hour_c
															 order by time_by_hour_c asc);
"""
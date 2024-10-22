channel_b_secondary_data_resampled_hour = """
create or replace view channel_b_secondary_data_resampled_hour as (select instrument_id as instrument_id_d,
														 		date_trunc('hour', time) as time_by_hour_d,
																	 round(avg(um3), 3) as um3_b,
																	 round(avg(um5), 3) as um5_b,
																	 round(avg(um1), 3) as um1_b,
																	 round(avg(um25), 3) as um25_b,
																	 round(avg(um50), 3) as um50_b,
																	 round(avg(um10), 3) as um10_b,
																	 round(avg(pm1_cf_1), 3) as pm1_cf_1_b,
																	 round(avg(pm10_cf_1), 3) as pm10_cf_1_b
														 from channel_b_secondary_data
														 group by 1, time_by_hour_d
														 order by time_by_hour_d asc);
"""
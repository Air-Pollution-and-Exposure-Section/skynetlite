insert_new_channel_b_secondary_data = """
create or replace function insert_new_channel_b_secondary_data(instrument_id int, my_latitude numeric, my_longitude numeric, location_type text) returns void as $function$
	begin
		insert into channel_b_secondary_data(instrument_id, time, latitude, longitude, um3, um5, um1, um25, um50, um10, PM1_cf_1, PM10_cf_1, device_location_type)
			with data_part as (select json_array_elements(json->'feeds') as jae from sanitized_json)
				select
					instrument_id as instrument_id,
					(jae->>'created_at')::timestamp as time,
					my_latitude as latitude,
					my_longitude as longitude,
					(jae->>'field1')::numeric as um3,
					(jae->>'field2')::numeric as um5,
					(jae->>'field3')::numeric as um1,
					(jae->>'field4')::numeric as um25,
					(jae->>'field5')::numeric as um50,
					(jae->>'field6')::numeric as um10,
					(jae->>'field7')::numeric as PM1_cf_1,
					(jae->>'field8')::numeric as PM10_cf_1,
					location_type as device_location_type
				from 
					data_part;
	end
$function$ language plpgsql;
"""
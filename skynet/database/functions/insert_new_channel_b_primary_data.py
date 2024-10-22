insert_new_channel_b_primary_data = """
create or replace function insert_new_channel_b_primary_data(instrument_id int, my_latitude numeric, my_longitude numeric, location_type text) returns void as $function$
	begin
		insert into channel_b_primary_data(instrument_id, time, latitude, longitude, PM1_atm, PM25_atm, PM10_atm, pressure, PM25_cf_1, device_location_type)
			with data_part as (select json_array_elements(json->'feeds') as jae from sanitized_json)
				select
					instrument_id as instrument_id,
					(jae->>'created_at')::timestamp as time,
					my_latitude as latitude,
					my_longitude as longitude,
					(jae->>'field1')::numeric as PM1_atm,
					(jae->>'field2')::numeric as PM25_atm,
					(jae->>'field3')::numeric as PM10_atm,
					(jae->>'field6')::numeric as pressure,
					(jae->>'field8')::numeric as PM25_cf_1,
					location_type as device_location_type
				from
					data_part;
	end
$function$ language plpgsql;
"""
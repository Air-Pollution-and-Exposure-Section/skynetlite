update_primary_data_with_dates = """
create or replace function update_primary_data_with_dates(my_instrument_id int, start_date text, end_date text) returns void as $function$
	declare
		thingspeak_id int;
		thingspeak_read_key text;
		number int;
		my_latitude numeric;
		my_longitude numeric;
		location_type text;
	begin
		-- GET THE SENSOR NUMBER
		number = my_instrument_id;
		-- GET THE IDs FOR CHANNEL A SENSOR
		select thingspeak_primary_id_a into thingspeak_id from purpleair_keys where instrument_id=number;
		select thingspeak_primary_id_read_key_a into thingspeak_read_key from purpleair_keys where instrument_id=number;
		-- GET THE LATITUDE AND LONGITUDE
		select latitude into my_latitude from instrument where id=number;
		select longitude into my_longitude from instrument where id=number;
		-- GET THE DEVICE LOCATION TYPE FROM THE INSTRUMENT TABLE
		select device_location_type into location_type from instrument where id=number;
		-- CLEAR THE TABLE
		truncate table raw_json;
		-- FOR CHANNEL A
		-- get the raw data
		execute get_raw_json(build_url_with_dates(thingspeak_id, thingspeak_read_key, start_date, end_date));
		raise notice 'Channel A -> Got data from (primary): %', build_url_with_dates(thingspeak_id, thingspeak_read_key, start_date, end_date);
		-- insert into the database
		execute insert_new_channel_a_primary_data(number, my_latitude, my_longitude, location_type);
		-- CLEAR THE TABLE
		truncate table raw_json;
		-- GET THE IDs CHANNEL B SENSOR
		select thingspeak_primary_id_b into thingspeak_id from purpleair_keys where instrument_id=number;
		select thingspeak_primary_id_read_key_b into thingspeak_read_key from purpleair_keys where instrument_id=number;
		-- FOR CHANNEL B
		-- get the raw data
		execute get_raw_json(build_url_with_dates(thingspeak_id, thingspeak_read_key, start_date, end_date));
		raise notice 'Channel B -> Got data from (primary): %', build_url_with_dates(thingspeak_id, thingspeak_read_key, start_date, end_date);
		-- insert into the database
		execute insert_new_channel_b_primary_data(number, my_latitude, my_longitude, location_type);
		-- CLEAR THE TABLE
		truncate table raw_json;
	end
$function$ language plpgsql;
"""
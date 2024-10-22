update_purpleair_sensor_data = """
create or replace function update_purpleair_sensor_data(instrument_id int) returns void as $function$
	declare
		number int;
	begin
		number = instrument_id;
		-- PRIMARY DATA QUERY
		execute update_primary_data(number);
		-- SECONDARY DATA QUERY
		execute update_secondary_data(number);
	end
$function$ language plpgsql;
"""
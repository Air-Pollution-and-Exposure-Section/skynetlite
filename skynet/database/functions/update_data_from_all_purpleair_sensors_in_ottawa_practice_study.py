update_data_from_all_purpleair_sensors_in_ottawa_practice_study = """
create or replace function update_data_from_all_online_purpleair_sensors_in_ottawa_practice_study() returns void as $function$
	declare
		row instrument%rowtype;
	begin
		for row in select * from online_instruments_in_ottawa_practice_study
			loop
				execute update_purpleair_sensor_data(row.id);
			end loop;
	end
$function$ language plpgsql;
"""
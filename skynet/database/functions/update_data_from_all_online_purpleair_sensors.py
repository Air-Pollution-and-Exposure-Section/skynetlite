update_data_from_all_online_purpleair_sensors = """
create or replace function update_data_from_all_online_purpleair_sensors() returns void as $function$
	declare
		row instrument%rowtype;
	begin
		for row in select * from instrument where is_online=True and ip_address is NULL
			loop
				execute update_purpleair_sensor_data(row.id);
			end loop;
	end
$function$ language plpgsql;
"""
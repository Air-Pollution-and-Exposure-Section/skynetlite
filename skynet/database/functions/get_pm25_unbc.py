get_pm25_unbc = """
create or replace function get_pm25_unbc(pa_cf_1 numeric, relative_humidity numeric) returns numeric as $function$
	begin
		if relative_humidity = 100 then
			relative_humidity = 99;
		end if;
		return pa_cf_1 / (1+ 0.24 / (100 / relative_humidity - 1));
	end
$function$ language plpgsql;
"""
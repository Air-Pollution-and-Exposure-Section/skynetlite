# -- RETURN THE EPA CORRECTED PM2.5 VALUE
get_pm25_epa = """
create or replace function get_pm25_epa(pa_cf_1 numeric, relative_humidity numeric) returns numeric as $function$
	begin
		if pa_cf_1<=343 then
			return 0.52*pa_cf_1 - 0.086*relative_humidity + 5.75;
		elsif pa_cf_1 > 343 then
			return 0.46*pa_cf_1 + 3.93*10^(-4)*pa_cf_1 + 2.97;
		else
			return NULL;
		end if;
	end
$function$ language plpgsql;
"""
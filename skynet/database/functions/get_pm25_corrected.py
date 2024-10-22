get_pm25_corrected = """
create or replace function get_pm25_corrected(first_num numeric, second_num numeric) returns numeric as $function$
	declare 
		average numeric;
	begin
		average = (first_num + second_num) / 2;
		if (average > 5) and (abs(first_num - second_num) > 0.5 * average) then
			return NULL;
		elseif (average <= 5) and (abs(first_num - second_num) > 5) then
			return NULL;
		else
			return average;
		end if;
	end
$function$ language plpgsql;
"""
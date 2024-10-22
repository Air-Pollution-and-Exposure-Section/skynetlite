get_average = """
create or replace function get_average(first_num numeric, second_num numeric) returns numeric as $function$
	begin
		return (first_num + second_num) / 2;
	end
$function$ language plpgsql;
"""
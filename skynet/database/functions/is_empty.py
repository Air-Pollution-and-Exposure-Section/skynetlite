is_empty = """
create or replace function is_empty() returns boolean as $function$
	declare
		number_of_rows int;
	begin
		select count(*) from get_rows_from_data_query into number_of_rows;
		if (number_of_rows = cast(0 as int)) then
			return True;
		end if;
		return False;
	end
$function$ language plpgsql;
"""
get_qa_average = """
-- RETURN QA'ed AVERAGE VALUE
create or replace function get_qa_average(first_num numeric, second_num numeric) returns numeric as $function$
	begin
		if first_num > 1000 then
			return second_num;
		elsif second_num > 1000 then
			return first_num;
		else
			return (first_num+second_num)/2;
		end if;
	end
$function$ language plpgsql;
"""
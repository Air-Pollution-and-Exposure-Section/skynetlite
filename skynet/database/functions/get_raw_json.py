# GET RAW JSON FUNCTION
get_raw_json = """
create or replace function get_raw_json(in url text) returns void as $function$
	declare
		exec_string text;
	begin
		truncate table raw_json;  
		exec_string := 'COPY raw_json FROM PROGRAM ''/usr/bin/curl "' || url || '"'';';
		execute exec_string;
	end
$function$ language plpgsql;
"""
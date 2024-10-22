# BUILDS THE THINGSPEAK URL BASED ON TODAYS DATE AND YESTERDAYS DATE
build_url_with_dates = """
create or replace function build_url_with_dates(thingspeak_id int, thingspeak_read_key text, start_date text, end_date text) returns text as $function$
	declare
		id int;
		read_key text;
		url_string text;
	begin
		id = thingspeak_id;
		read_key = thingspeak_read_key;
		url_string = 'https://thingspeak.com/channels/'||id||'/feeds.json?api_key='||read_key||'&start='||start_date||'&end='||end_date;
		return url_string;
	end
$function$ language plpgsql;
"""
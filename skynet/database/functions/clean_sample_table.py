clean_sample_table = """
create or replace function clean_sample_tables() returns void as $function$
	begin
		update sample set season = '' where season = 'None';
		update sample set page_comments = '' where page_comments = 'nan';
		update sample set comments = '' where comments = 'nan';
		update sample set page_comments = '' where page_comments = 'None';
		update sample set comments = '' where comments = 'None';
		update sample set City = '' where City = 'None';
		update sample set dc_pah = '' where dc_pah = 'None';
		update sample set ss_pah = '' where ss_pah = 'None';
	end
$function$ language plpgsql;
"""
data_pull = """
create or replace function data_pull(instrument_id int, start_date text, end_date text) returns void as $function$
	begin
		execute update_primary_data_with_dates(instrument_id, start_date, end_date);
		execute update_secondary_data_with_dates(instrument_id, start_date, end_date);
	end
$function$ language plpgsql;
"""
end_responsibility = """
create or replace function end_responsibility(participant_id int, instrument_id int) returns void as $function$
	declare
		my_participant_id int;
		my_instrument_id int;
	begin
		my_participant_id = participant_id;
		my_instrument_id = instrument_id;
		update responsibility set end_date = date'today' where responsibility.participant_id=my_participant_id and responsibility.instrument_id=my_instrument_id;
	end
$function$ language plpgsql;
"""
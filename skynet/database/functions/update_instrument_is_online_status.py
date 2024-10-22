update_instrument_is_online_status = """
create or replace function update_instrument_is_online_status() returns void as $function$
	declare
		row purpleair_keys%rowtype;
		channel_a_primary_check boolean;
		channel_a_secondary_check boolean;
		channel_b_primary_check boolean;
		channel_b_secondary_check boolean;
	begin
		for row in select * from purpleair_keys
			loop
				raise notice 'Checking instrument ID: % ...', row.instrument_id;
				-- check the primary data on channel a
				truncate table raw_json;
				execute get_raw_json(build_url(row.thingspeak_primary_id_a, row.thingspeak_primary_id_read_key_a));
				select is_empty() into channel_a_primary_check;
				truncate table raw_json;
				-- check the secondary data on channel a
				truncate table raw_json;
				execute get_raw_json(build_url(row.thingspeak_secondary_id_a, row.thingspeak_secondary_id_read_key_a));
				select is_empty() into channel_a_secondary_check;
				truncate table raw_json;
				-- check the primary data on channel b
				truncate table raw_json;
				execute get_raw_json(build_url(row.thingspeak_primary_id_b, row.thingspeak_primary_id_read_key_b));
				select is_empty() into channel_b_primary_check;
				truncate table raw_json;
				-- check the secondary data on channel b
				truncate table raw_json;
				execute get_raw_json(build_url(row.thingspeak_primary_id_b, row.thingspeak_primary_id_read_key_b));
				select is_empty() into channel_b_secondary_check;
				truncate table raw_json;
				raise notice '% % % %', channel_a_primary_check, channel_a_secondary_check, channel_b_primary_check, channel_b_secondary_check;
				-- UPDATE THE IS_ONLINE STATUS IN THE INSTRUMENT TABLE
				if (channel_a_primary_check = True and channel_a_secondary_check = True and channel_b_primary_check = True and channel_b_secondary_check = True) then
					update instrument set is_online = False where id = row.instrument_id;
				else
					raise notice 'Updating instrument %', row.instrument_id;
					update instrument set is_online = True where id=row.instrument_id;
				end if;
				raise notice 'Done checking instrument ID: %', row.instrument_id;
				raise notice '';
			end loop;
	end
$function$ language plpgsql;
"""
online_instruments_in_ottawa_practice_study = """
create or replace view online_instruments_in_ottawa_practice_study as (select responsibility.instrument_id from participation 
																	   inner join responsibility on participation.participant_id = responsibility.participant_id 
																	   inner join instrument on responsibility.instrument_id = instrument.id where participation.study_id = 1 and instrument.is_online=True 
																	   group by responsibility.instrument_id, participation.study_id);
"""
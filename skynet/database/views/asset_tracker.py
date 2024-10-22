asset_tracker = """
CREATE OR REPLACE VIEW asset_tracker AS
SELECT participant.first_name, 
       participant.last_name,
       instrument.manufacturer AS instrument_manufacturer,
       instrument.mac_address,
       instrument.label AS instrument_label,
       sample.eas_sample_id,
       responsibility.start_date,
       responsibility.end_date,
       study.name AS study
FROM responsibility
INNER JOIN participant ON responsibility.participant_id = participant.id
FULL OUTER JOIN instrument ON responsibility.instrument_id = instrument.id
FULL OUTER JOIN sample ON responsibility.sample_id = sample.id
FULL OUTER JOIN participation ON responsibility.participant_id = participation.participant_id
INNER JOIN study ON participation.study_id = study.id;
"""
update_online_status = """
CREATE OR REPLACE FUNCTION update_online_status()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the most recent record's date for the current instrument is more than an hour old
    IF (SELECT MAX(date) FROM temperature WHERE instrument_id = NEW.instrument_id) < (CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - INTERVAL '1 hour') THEN
        -- Set online status to false
        UPDATE instrument
        SET online = false
        WHERE id = NEW.instrument_id;
    ELSE
        -- Set online status to true
        UPDATE instrument
        SET online = true
        WHERE id = NEW.instrument_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
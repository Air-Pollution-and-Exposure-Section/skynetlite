log_status_change = """
CREATE OR REPLACE FUNCTION log_status_change()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.online IS DISTINCT FROM OLD.online THEN
            INSERT INTO instrument_online_history (instrument_id, online)
            VALUES (NEW.id, NEW.online);
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
"""
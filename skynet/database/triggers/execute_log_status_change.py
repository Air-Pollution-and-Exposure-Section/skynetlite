execute_log_status_change = """
CREATE TRIGGER execute_log_status_change
AFTER UPDATE ON instrument
FOR EACH ROW
EXECUTE FUNCTION log_status_change();
"""
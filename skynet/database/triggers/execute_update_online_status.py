execute_upate_online_status = """
CREATE TRIGGER execute_update_online_status
AFTER INSERT OR UPDATE ON temperature
FOR EACH ROW
EXECUTE FUNCTION update_online_status();
"""
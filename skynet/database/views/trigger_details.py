trigger_details = """
CREATE VIEW trigger_details AS
SELECT                                        
    tgname AS trigger_name,
    relname AS table_name,
    pg_catalog.pg_get_triggerdef(pg_trigger.oid) AS definition
FROM 
    pg_trigger
JOIN 
    pg_class ON pg_trigger.tgrelid = pg_class.oid
WHERE 
    NOT tgisinternal;  -- Excludes internally defined triggers
"""
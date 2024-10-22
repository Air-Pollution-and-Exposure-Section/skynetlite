sanitized_json = """
create or replace view sanitized_json as (select replace(replace(raw_json.json::text,'',''::text),'',''::text)::json AS json FROM raw_json);
"""
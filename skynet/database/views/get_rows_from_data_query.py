get_rows_from_data_query = """
create or replace view get_rows_from_data_query as (select json_array_elements(json->'feeds') as jae from sanitized_json);
"""
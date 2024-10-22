#!/usr/bin/env python3
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

# IMPORT THE DATABASE CONNECTION
# This is needed to direct the script to the appropriate database to build
from skynet.database.config import DATABASE_URI

# Enable logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(DATABASE_URI, echo=True)

# Define the raw SQL query
sql_query = """
WITH recent_records AS (
    SELECT 
        instrument_id, 
        date
    FROM (
        SELECT 
            instrument_id,
            date, 
            ROW_NUMBER() OVER (PARTITION BY instrument_id ORDER BY date DESC) AS rn
        FROM 
            temperature
    ) subquery
    WHERE 
        rn = 1
)
UPDATE temperature
SET instrument_id = temperature.instrument_id
FROM recent_records
WHERE temperature.instrument_id = recent_records.instrument_id
  AND temperature.date = recent_records.date;
"""

# Execute the query using the engine with exception handling
try:
    with engine.connect() as connection:
        with connection.begin():  # Begin a transaction
            connection.execute(text(sql_query))
except DBAPIError as e:
    print(f"A database error occurred: {e}")
    if e.orig:
        print(f"Original error: {e.orig}")
except SQLAlchemyError as e:
    print(f"An error occurred with SQLAlchemy: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

#!/usr/bin/env python3
from sqlalchemy import create_engine, text
from skynet.database.Base import Base
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

# ANSI escape code to reset the color to default
RESET = "\033[0m"
BLUE = "\033[34m\033[1m"  # Standard dark blue with bold for emphasis

# IMPORT THE DATABASE CONNECTION
# This is needed to direct the script to the appropriate database to build
from skynet.database.config import DATABASE_URI

# import the tables
from skynet.database.tables import Instrument
from skynet.database.tables import CO2
from skynet.database.tables import Exposure
from skynet.database.tables import FieldDataCodes
from skynet.database.tables import Humidity
from skynet.database.tables import Location
from skynet.database.tables import Participant
from skynet.database.tables import Particulate
from skynet.database.tables import Pressure
from skynet.database.tables import PurpleAirKeys
from skynet.database.tables import Sample
from skynet.database.tables import Site
from skynet.database.tables import Substance
from skynet.database.tables import Temperature
from skynet.database.tables import Study
from skynet.database.tables import Responsibility
from skynet.database.tables import Emails
from skynet.database.tables import EmailLogs
from skynet.database.tables.InstrumentOnlineHistory import InstrumentOnlineHistory

# import the functions
from skynet.database.functions.build_url import build_url
from skynet.database.functions.build_url_with_dates import build_url_with_dates
from skynet.database.functions.clean_sample_table import clean_sample_table
from skynet.database.functions.data_pull import data_pull
from skynet.database.functions.end_responsibility import end_responsibility
from skynet.database.functions.get_average import get_average
from skynet.database.functions.get_pm25_corrected import get_pm25_corrected
from skynet.database.functions.get_pm25_epa import get_pm25_epa
from skynet.database.functions.get_pm25_unbc import get_pm25_unbc
from skynet.database.functions.get_qa_average import get_qa_average
from skynet.database.functions.get_raw_json import get_raw_json
from skynet.database.functions.insert_new_channel_a_primary_data import insert_new_channel_a_primary_data
from skynet.database.functions.insert_new_channel_a_secondary_data import insert_new_channel_a_secondary_data
from skynet.database.functions.insert_new_channel_b_primary_data import insert_new_channel_b_primary_data
from skynet.database.functions.insert_new_channel_b_secondary_data import insert_new_channel_b_secondary_data
from skynet.database.functions.is_empty import is_empty
from skynet.database.functions.update_data_from_all_online_purpleair_sensors import update_data_from_all_online_purpleair_sensors
from skynet.database.functions.update_data_from_all_purpleair_sensors_in_ottawa_practice_study import update_data_from_all_purpleair_sensors_in_ottawa_practice_study
from skynet.database.functions.update_instrument_is_online_status import update_instrument_is_online_status
from skynet.database.functions.update_primary_data_with_dates import update_primary_data_with_dates
from skynet.database.functions.update_primary_data import update_primary_data
from skynet.database.functions.update_purpleair_sensor_data import update_purpleair_sensor_data
from skynet.database.functions.update_secondary_data_with_dates import update_secondary_data_with_dates
from skynet.database.functions.update_secondary_data import update_secondary_data
from skynet.database.functions.log_status_change import log_status_change
from skynet.database.functions.update_online_status import update_online_status

# import the triggers
from skynet.database.triggers.execute_log_status_change import execute_log_status_change
from skynet.database.triggers.execute_update_online_status import execute_upate_online_status

# import the views
from skynet.database.views.realtime_instruments import realtime_instruments
from skynet.database.views.trigger_details import trigger_details

funcs = [
    build_url,
    build_url_with_dates,
    clean_sample_table,
    data_pull,
    end_responsibility,
    get_average,
    get_pm25_corrected,
    get_pm25_epa,
    get_pm25_unbc,
    get_qa_average,
    get_raw_json,
    insert_new_channel_a_primary_data,
    insert_new_channel_a_secondary_data,
    insert_new_channel_b_primary_data,
    insert_new_channel_b_secondary_data,
    is_empty,
    update_data_from_all_online_purpleair_sensors,
    update_data_from_all_purpleair_sensors_in_ottawa_practice_study,
    update_instrument_is_online_status,
    update_primary_data_with_dates,
    update_primary_data,
    update_purpleair_sensor_data,
    update_secondary_data_with_dates,
    update_secondary_data,
    log_status_change,
    update_online_status,
]

triggers = [
       execute_log_status_change,
       execute_upate_online_status
]

engine = create_engine(DATABASE_URI, echo=True)

### BUILD THE TABLES
Base.metadata.create_all(engine)

"""
--- Comment from Jonathan (30 Apr 2024)
I couldn't figure out how to make the table instrument_online_history using SQL Alchemy in the same way as the other ones
So I decalred it using a string and building it in the database in the same way as views, functions, triggers.
"""
tables = [
      InstrumentOnlineHistory,
]

for table in tables:
    with engine.begin() as connection:
        try:
            connection.execute(text(table))
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")

### BUILD THE VIEWS
views = [
      realtime_instruments,
      trigger_details,
]

for view in views:
    with engine.begin() as connection:
        try:
            connection.execute(text(view))
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")

### BUILD THE FUNCTIONS
for func in funcs:
    with engine.begin() as connection:
        try:
            connection.execute(text(func))
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")

### BUILD THE TRIGGERS
for trigger in triggers:
    with engine.begin() as connection:
        try:
            connection.execute(text(trigger))
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")

def load_data(data:pd.DataFrame, db_table:str, connection):
    try:
        data.to_sql(name=db_table, con=engine, if_exists='append', index=False)
    except UniqueViolation as e:
        print(e)
    except IntegrityError as e:
        print(e)


data_dir = 'skynet/database/seed_data'

# import the instrument data
print(f"{BLUE}'\nImporting the instrument table'{RESET}")
data = pd.read_csv(f'{data_dir}/instrument.csv')
load_data(data, 'instrument', engine)
print(f"{BLUE}'Done!\n'{RESET}")

with engine.connect() as connection:
    connection.execute(text("SELECT setval('instrument_id_seq', (SELECT MAX(id) FROM instrument))"))

# import the participant data
print(f"{BLUE}'\nImporting the participant table'{RESET}")
data = pd.read_csv(f'{data_dir}/participant.csv')
load_data(data, 'participant', engine)
print(f"{BLUE}'Done!\n'{RESET}")

with engine.connect() as connection:
	connection.execute(text("SELECT setval('participant_id_seq', (SELECT MAX(id) FROM participant))"))

# import the study data
print(f"{BLUE}'\nImporting the study table'{RESET}")
data = pd.read_csv(f'{data_dir}/study.csv')
load_data(data, 'study', engine)
print(f"{BLUE}'Done!\n'{RESET}")

with engine.connect() as connection:
    connection.execute(text("SELECT setval('study_id_seq', (SELECT MAX(id) FROM study))"))

# import the purpleair_keys data
print(f"{BLUE}'\nImporting the purpleair keys table'{RESET}")
data = pd.read_csv(f'{data_dir}/purpleair_keys.csv')
load_data(data, 'purpleair_keys', engine)
print(f"{BLUE}'Done!\n'{RESET}")

with engine.connect() as connection:
		connection.execute(text("SELECT setval('purpleair_keys_id_seq', (SELECT MAX(id) FROM purpleair_keys))"))

# import the responsibility data
print(f"{BLUE}'\nImporting the responsibility table ...'{RESET}")
data = pd.read_csv(f'{data_dir}/responsibility.csv')
load_data(data, 'responsibility', engine)
print(f"{BLUE}'Done!\n'{RESET}")

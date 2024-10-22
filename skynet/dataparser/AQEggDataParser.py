from skynet.database.config import AQEGG_API_KEY as READ_KEY
import json
import requests
from datetime import datetime

# import database tables
from skynet.database.tables.Instrument import Instrument
from skynet.database.tables.PurpleAirKeys import PurpleAirKeys

""" import database handler to find the instrument_id corresponding to the serial_number
column in the instrument table
"""
from skynet.handler.Handler import Handler


class AQEggDataParser:
    def __init__(self):
        # This will hold the parsed data
        self.__data = {}

    def parse(self, data):
            # Start a session for database queries
            dbHandler = Handler()
            dbHandler.start_session()

            for key, value in data.items():
                try:
                    details = json.loads(value)
                    serial_number = key

                    # Query the instrument ID from Instrument table
                    instrument_query = dbHandler.session.query(Instrument.id).filter(Instrument.serial_number == serial_number).first()
                    if instrument_query:
                        instrument_id = instrument_query.id
                    else:
                        # Optionally handle the case where no instrument ID is found
                        instrument_id
                        print(f"No instrument ID found for serial_number {serial_number}")

                    # Extracting timestamp information
                    last_seen_dt = details.get('last_report', '2024-04-18T17:44:43.111Z')
                    last_seen = int(datetime.strptime(last_seen_dt, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())

                    # Extracting and structuring humidity, temperature, and pressure data
                    humidity = {
                        'date' : details.get('humidity', {}).get('date'),
                        'raw': details.get('humidity', {}).get('raw-value'),
                        'converted': details.get('humidity', {}).get('converted-value'),
                        'units': details.get('humidity', {}).get('raw-units', 'percent')
                    }
                    temperature = {
                        'date' : details.get('temperature', {}).get('date'),
                        'raw': details.get('temperature', {}).get('raw-value'),
                        'converted': details.get('temperature', {}).get('converted-value'),
                        'units': details.get('temperature', {}).get('raw-units', 'degC')
                    }
                    pressure = {
                        'date' : details.get('pressure', {}).get('date'),
                        'value': details.get('pressure', {}).get('pressure'),
                        'units': details.get('pressure', {}).get('pressure-units', 'Pa')
                    }

                    # Extracting CO2 data
                    co2 = {
                        'date' : details.get('co2', {}).get('date'),
                        'comp_val': details.get('co2', {}).get('compensated-value'),
                        'units': details.get('co2', {}).get('converted-units', 'ppm')
                    }

                    # Extracting exposure data
                    exposure = {
                        'date' : details.get('exposure', {}).get('date'),
                        'value': details.get('exposure', {}).get('value'),
                    }

                    # Handling particulate matter data
                    pm_info = details.get('full_particulate', {})
                    pm_counts = {
                        'date' : details.get('full_particulate', {}).get('date'),
                        '0.3_um_count': [pm_info.get('pm0p3_cpl_a'), pm_info.get('pm0p3_cpl_b')],
                        '0.5_um_count': [pm_info.get('pm0p5_cpl_a'), pm_info.get('pm0p5_cpl_b')],
                        '1.0_um_count': [pm_info.get('pm1p0_cpl_a'), pm_info.get('pm1p0_cpl_b')],
                        '2.5_um_count': [pm_info.get('pm2p5_cpl_a'), pm_info.get('pm2p5_cpl_b')],
                        '5.0_um_count': [pm_info.get('pm5p0_cpl_a'), pm_info.get('pm5p0_cpl_b')],
                        '10.0_um_count': [pm_info.get('pm10p0_cpl_a'), pm_info.get('pm10p0_cpl_b')],
                        'pm1.0_cf_1' : [pm_info.get('pm1p0_cf1_a'), pm_info.get('pm1p0_cf1_b')],
                        'pm1.0_atm' : [pm_info.get('pm1p0_atm_a'), pm_info.get('pm1p0_atm_b')],
                        'pm2.5_atm': [pm_info.get('pm2p5_atm_a'), pm_info.get('pm2p5_atm_b')],
                        'pm2.5_cf_1': [pm_info.get('pm2p5_cf1_a'), pm_info.get('pm2p5_cf1_b')],
                        'pm10.0_cf_1' : [pm_info.get('pm10p0_cf1_a'), pm_info.get('pm10p0_cf1_b')],
                        'pm10.0_atm' : [pm_info.get('pm10p0_atm_a'), pm_info.get('pm10p0_atm_b')],
                    }

                    # Storing data with serial number as key
                    self.__data[serial_number] = {
                        'serial_number': serial_number,
                        'instrument_id':instrument_id,
                        'last_seen': last_seen,
                        'last_seen_dt': last_seen_dt,
                        'humidity': humidity,
                        'temperature': temperature,
                        'pressure': pressure,
                        'co2': co2,
                        'exposure': exposure,
                        **pm_counts
                    }
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing data for sensor {key}: {e}")

            dbHandler.close_session()

    def get_data(self):
        return self.__data

    def get_data(self):
        return self.__data
    
    def sensors(self) -> list:
        return [k for k in self.__data.keys()]
    
    """FOR AQEggs the tag=serial_number"""
    def get_sensor_data(self, tag) -> dict:
        return self.__data[tag] 

if __name__ == '__main__':
    pass

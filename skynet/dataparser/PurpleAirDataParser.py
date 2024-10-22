#!/usr/bin/env python3
from datetime import datetime, timezone
import json

# import database tables
from skynet.database.tables.PurpleAirKeys import PurpleAirKeys

""" import database handler to find the instrument_id corresponding to the sensor_index=sensor_id_a
value in the PurpleAirKeys table
"""
from skynet.handler.Handler import Handler

class PurpleAirDataParser():
    def __init__(self):
        self.__data = {}
        self.group_id = None

    def _td(self, timestamp):
        """Convert timestamp to datetime object."""
        # milliseconds are sufficient, [:-3] removes the microseconds keeps the td to milliseconds
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def parse(self, raw_data):
        json_data = json.loads(raw_data)

        self.group_id = json_data['group_id']
        fields = json_data['fields']
        self.__data = {}

        # Start a session for database queries
        dbHandler = Handler()
        dbHandler.start_session()

        for sensor_data in json_data['data']:
            sensor_index = sensor_data[0]
            self.__data[sensor_index] = {'sensor_index': sensor_index}

            # Query the instrument ID from PurpleAirKeys table
            instrument_query = dbHandler.session.query(PurpleAirKeys.instrument_id).filter(PurpleAirKeys.sensor_id_a == sensor_index).first()
            if instrument_query:
                self.__data[sensor_index]['instrument_id'] = instrument_query.instrument_id
            else:
                # Optionally handle the case where no instrument ID is found
                self.__data[sensor_index]['instrument_id'] = None
                print(f"No instrument ID found for sensor index {sensor_index}")

            for k, v in enumerate(sensor_data):
                if fields[k].count('um_count_a') or fields[k].count('pm2.5_atm_a') or fields[k].count('pm2.5_cf_1_a'):
                    self.__data[sensor_index][fields[k][:-2]] = [float(v), float(sensor_data[k+1])]
                elif fields[k].count('um_count_b') or fields[k].count('pm2.5_atm_b') or fields[k].count('pm2.5_cf_1_b'):
                    continue  # Skip 'b' fields based on your original design
                elif fields[k] in ['humidity_a', 'pressure_a', 'temperature_a']:
                    self.__data[sensor_index][fields[k][:-2]] = v
                elif fields[k] == 'last_seen':
                    # Format the datetime object as a string
                    self.__data[sensor_index]['last_seen'] = v
                    self.__data[sensor_index]['last_seen_dt'] = self._td(v)
                else:
                    self.__data[sensor_index][fields[k]] = v

        # Close session after processing all data
        dbHandler.close_session()

    def get_data(self):
        """Return parsed data."""
        return self.__data

    def __len__(self) -> int:
        len([k for k in self.__data.keys()])

    def sensors(self) -> list:
        return [k for k in self.__data.keys()]

    def get_sensor_data(self, tag) -> dict:
        return self.__data[tag]
    
    def sensor_last_seen(self, sensor_id:int, string:bool=False):
        if string:
            return self.__data[sensor_id]['last_seen_dt']
        return self.__data[sensor_id]['last_seen']

    def sensor_humidity(self, sensor_id:int) -> float:
        return self.__data[sensor_id]['humidity']
    
    def sensor_temperature(self, sensor_id:int) -> float:
        return self.__data[sensor_id]['temperature']
    
    def sensor_pressure(self, sensor_id:int) -> float:
        return self.__data[sensor_id]['pressure']

    def sensor_mass(self, sensor_id:int, variant:str) -> list:
        assert variant in ['atm', 'cf_1']
        return self.__data[sensor_id]['pm2.5_' + variant]
    
    def sensor_mass_ch(self, sensor_id:int, variant:str, channel:str) -> float:
        assert variant in ['atm', 'cf_1']
        assert channel in ['a', 'b']
        return self.__data[sensor_id]['pm2.5_' + variant][0 if channel == 'a' else 1]
    
    def sensor_count(self, sensor_id:int, size:str) -> list:
        assert size in ['0.3', '0.5', '1.0', '2.5']
        return self.__data[sensor_id][size + '_um_count']

    def sensor_count_ch(self, sensor_id:int, size:str, channel:str) -> float:
        assert size in ['0.3', '0.5', '1.0', '2.5']
        assert channel in ['a', 'b']
        return self.__data[sensor_id][size + '_um_count'][0 if channel == 'a' else 1]
    

if __name__=="__main__":
    pass
#!/usr/bin/env python3
from sqlalchemy import create_engine
from skynet.database.config import DBNAME, USER, PASSWORD, HOST, PORT
from sqlalchemy.orm import sessionmaker

# Error handling
from sqlalchemy.exc import IntegrityError

# import the skynet tables
from skynet.database.tables.Instrument import Instrument
from skynet.database.tables.Humidity import Humidity
from skynet.database.tables.Temperature import Temperature
from skynet.database.tables.Pressure import Pressure
from skynet.database.tables.CO2 import CO2
from skynet.database.tables.Exposure import Exposure
from skynet.database.tables.Particulate import Particulate

class Handler():
    def __init__(self) -> None:
        self.USER = USER
        self.DBNAME = DBNAME
        DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
        self.echo_state = True
        self.engine = create_engine(DATABASE_URI, echo=self.echo_state)
        self.session = None

    def start_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None
        else:
            print("No session to close")

    """New humidity data requires a type flag for the function.
    This is because the humidity record is different depending on the instrument

    PurpleAir:
    'humidity': 27

    AQEgg
    'humidity': {'raw': 48.863, 'converted': 51.649, 'units': 'percent'}

    (1) See here https://api.purpleair.com/#api-sensors-get-sensor-data for Purple Air API reference
    (2) See here https://airqualityegg.com/api-docs/#/developers/messagesByTopic for AQEgg API reference

    
    type == 0 -> PurpleAir
    type == 1 -> AQEgg
    """
    def insert_humidity_data(self, sensor_data:dict, type:int):
        if type==0:
            new_humidity = Humidity(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['last_seen_dt'],
                raw_val=sensor_data['humidity'],
                conv_val = None,
                unit='percent'
            )
        else:
            humidityData = sensor_data['humidity']
            new_humidity = Humidity(
                instrument_id=sensor_data['instrument_id'],
                date=humidityData['date'],
                raw_val=humidityData['raw'],
                conv_val=humidityData['converted'],
                unit=humidityData['units']
            )
        try:
            self.session.add(new_humidity)
            self.session.commit()
            print("Humidity data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert humidity data due to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert humidity data: {e}")

    """New temperature data requires a type flag for the function.
    This is because the temperature measurement for PurpleAirs is in degF
    and the temeprature measurement for AQEggs is in degC.

    (1) See here https://api.purpleair.com/#api-sensors-get-sensor-data for Purple Air API reference
    (2) See here https://airqualityegg.com/api-docs/#/developers/messagesByTopic for AQEgg API reference

    type == 0 -> PurpleAir
    type == 1 -> AQEgg
    """
    def insert_temperature_data(self, sensor_data:dict, type:int):
        # if data from purpleair -> type == 0
        if type == 0:
            new_temperature = Temperature(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['last_seen_dt'],
                raw_val=sensor_data['temperature'],
                conv_val = None,
                unit='degF'
            )
        # else data from aqegg -> type == 1
        else:
            tempData = sensor_data['temperature']
            new_temperature = Temperature(
                instrument_id=sensor_data['instrument_id'],
                date=tempData['date'],
                raw_val=tempData['raw'],
                conv_val=tempData['converted'],
                unit=tempData['units']
            )
        try:
            self.session.add(new_temperature)
            self.session.commit()
            print("Temperature data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert temperature data due to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert temperature data: {e}")

    """New pressure data requires a type flag for the function.
    This is because the pressure measurement for purpleairs is in mbar
    and the pressure measurement for aqeggs is in Pa.

    (1) See here https://api.purpleair.com/#api-sensors-get-sensor-data for Purple Air API reference
    (2) See here https://airqualityegg.com/api-docs/#/developers/messagesByTopic for AQEgg API reference

    type == 0 -> PurpleAir
    type == 1 -> AQEgg
    """
    def insert_pressure_data(self, sensor_data:dict, type:int):
        if type == 0:
            new_pressure = Pressure(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['last_seen_dt'],
                val=sensor_data['pressure'],
                unit='mbar'
            )
        else:
            pressureData = sensor_data['pressure']
            new_pressure = Pressure(
                instrument_id=sensor_data['instrument_id'],
                date=pressureData['date'],
                val=pressureData['value'],
                unit=pressureData['units']
            )
        try:
            self.session.add(new_pressure)
            self.session.commit()
            print("Pressure data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert pressure data due to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert pressure data: {e}")

    """New particulate data requires a type flag for the function.
    This is because the particulate counts for purpleairs are reported in particles/100ml
    and the particulate counts for aqeggs is in counts/dL.

    Yes, it is true that particles/100ml = counts/dL but for the sake
    of being careful added logic is added to save these as reported by the instrument APIs. 
    In the future this will most likely be reported in counts/dL.

    (1) See here https://api.purpleair.com/#api-sensors-get-sensor-data for Purple Air API reference
    (2) See here https://airqualityegg.com/api-docs/#/developers/messagesByTopic for AQEgg API reference

    type == 0 -> PurpleAir
    type == 1 -> AQEgg
    """
    def insert_particulate_data(self, sensor_data:dict, type:int): 
        if type == 0:
            # Define units
            pm_units_cf1 = 'ug/m^3'
            pm_units_atm = 'ug/m^3'
            pm_units_counts = 'particles/100ml'
            
            # Prepare data for Channel A
            pm_data_a = Particulate(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['last_seen_dt'],
                pm2p5_cf1=sensor_data['pm2.5_cf_1'][0],
                pm2p5_atm=sensor_data['pm2.5_atm'][0],
                pm0p3_counts=sensor_data['0.3_um_count'][0],
                pm0p5_counts=sensor_data['0.5_um_count'][0],
                pm1p0_counts=sensor_data['1.0_um_count'][0],
                pm2p5_counts=sensor_data['2.5_um_count'][0],
                pm_cf1_units=pm_units_cf1,
                pm_atm_units=pm_units_atm,
                pm_counts_units=pm_units_counts,
                channel='a'
            )

            # Prepare data for Channel B
            pm_data_b = Particulate(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['last_seen_dt'],
                pm2p5_cf1=sensor_data['pm2.5_cf_1'][1],
                pm2p5_atm=sensor_data['pm2.5_atm'][1],
                pm0p3_counts=sensor_data['0.3_um_count'][1],
                pm0p5_counts=sensor_data['0.5_um_count'][1],
                pm1p0_counts=sensor_data['1.0_um_count'][1],
                pm2p5_counts=sensor_data['2.5_um_count'][1],
                pm_cf1_units=pm_units_cf1,
                pm_atm_units=pm_units_atm,
                pm_counts_units=pm_units_counts,
                channel='b'
            )

        else:
            # Define units
            pm_units_cf1 = 'ug/m^3'
            pm_units_atm = 'ug/m^3'
            pm_units_counts = "counts/dL"

            # Prepare data for Channel A
            pm_data_a = Particulate(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['date'],
                pm1p0_cf1=sensor_data['pm1.0_cf_1'][0],
                pm1p0_atm=sensor_data['pm1.0_atm'][0],
                pm2p5_cf1=sensor_data['pm2.5_cf_1'][0],
                pm2p5_atm=sensor_data['pm2.5_atm'][0],
                pm10p0_cf1=sensor_data['pm10.0_cf_1'][0],
                pm10p0_atm=sensor_data['pm10.0_atm'][0],
                pm0p3_counts=sensor_data['0.3_um_count'][0],
                pm0p5_counts=sensor_data['0.5_um_count'][0],
                pm1p0_counts=sensor_data['1.0_um_count'][0],
                pm2p5_counts=sensor_data['2.5_um_count'][0],
                pm5p0_counts=sensor_data['5.0_um_count'][0],
                pm10p0_counts=sensor_data['10.0_um_count'][0],
                pm_cf1_units=pm_units_cf1,
                pm_atm_units=pm_units_atm,
                pm_counts_units=pm_units_counts,
                channel='a'
            )

            # Prepare data for Channel B
            pm_data_b = Particulate(
                instrument_id=sensor_data['instrument_id'],
                date=sensor_data['date'],
                pm1p0_cf1=sensor_data['pm1.0_cf_1'][1],
                pm1p0_atm=sensor_data['pm1.0_atm'][1],
                pm2p5_cf1=sensor_data['pm2.5_cf_1'][1],
                pm2p5_atm=sensor_data['pm2.5_atm'][1],
                pm10p0_cf1=sensor_data['pm10.0_cf_1'][1],
                pm10p0_atm=sensor_data['pm10.0_atm'][1],
                pm0p3_counts=sensor_data['0.3_um_count'][1],
                pm0p5_counts=sensor_data['0.5_um_count'][1],
                pm1p0_counts=sensor_data['1.0_um_count'][1],
                pm2p5_counts=sensor_data['2.5_um_count'][1],
                pm5p0_counts=sensor_data['5.0_um_count'][1],
                pm10p0_counts=sensor_data['10.0_um_count'][1],
                pm_cf1_units=pm_units_cf1,
                pm_atm_units=pm_units_atm,
                pm_counts_units=pm_units_counts,
                channel='b'
            )
        try:
            # Try inserting Channel A data
            self.session.add(pm_data_a)
            self.session.commit()
            print("Channel A PM data inserted successfully.")

        except IntegrityError:
            self.session.rollback()
            print("Failed to insert Channel A PM data to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert Channel A PM data: {e}")

        try:
            # Try inserting Channel B data
            self.session.add(pm_data_b)
            self.session.commit()
            print("Channel B PM data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert Channel B PM data to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert Channel B PM data: {e}")

    """Purple Air instruments do not report co2 values
    This only needs to be implemented for the AQEgg.
    """
    def insert_co2_data(self, sensor_data):
        co2Data = sensor_data['co2']
        new_co2 = CO2(
            instrument_id=sensor_data['instrument_id'],
            date=co2Data['date'],
            comp_val=co2Data['comp_val'],
            unit=co2Data['units']
        )
        try:
            self.session.add(new_co2)
            self.session.commit()
            print("CO2 data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert co2 data due to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert co2 data: {e}")


    def insert_exposure_data(self, sensor_data):
        expData = sensor_data['exposure']
        newExposure = Exposure(
            instrument_id=sensor_data['instrument_id'],
            date = expData['date'],
            val = expData['value']
        )
        try:
            self.session.add(newExposure)
            self.session.commit()
            print("Exposure data inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            print("Failed to insert exposure data due to integrity error.")
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert exposure data: {e}")

    def insert_new_purpleair_data(self, sensor_data:dict):
        # Start a session with the database
        self.start_session()
        self.insert_humidity_data(sensor_data, type=0)
        self.insert_temperature_data(sensor_data, type=0) # type = 0 for Purple Airs
        self.insert_pressure_data(sensor_data, type=0) # type = 0 for Purple Airs
        self.insert_particulate_data(sensor_data, type=0) # type = 0 for Purple Airs
        # close the session with the database
        self.close_session()

    def insert_new_aqegg_data(self, sensor_data:dict):
        # start session
        self.start_session()
        self.insert_humidity_data(sensor_data, type=1)
        self.insert_temperature_data(sensor_data, type=1)
        self.insert_pressure_data(sensor_data, type=1)
        self.insert_particulate_data(sensor_data, type=1)
        self.insert_co2_data(sensor_data)
        self.insert_exposure_data(sensor_data)
        # close session
        self.close_session()

    ### TO BE IMPLEMENTED ###
    def insert_new_eahmu_data(self, sensor_data:dict):
        pass

if __name__=="__main__":
    pass

# aqgg auths
from skynet.database.config import AQEGG_API_KEY as api_key
from skynet.fetcher.AQEggFetcher import AQEggFetcher
from skynet.dataparser.AQEggDataParser import AQEggDataParser
from skynet.handler.Handler import Handler
from skynet.database.tables.Instrument import Instrument


if __name__=="__main__":
    # create a database handler
    dbHandler = Handler()
    # create an AQ Egg fetcher object
    fetcher = AQEggFetcher(api_key=api_key)
    # get all the AQ Egg instruments in the database
    dbHandler.start_session()
    instrument_query = dbHandler.session.query(Instrument.serial_number).\
                    filter(Instrument.name == "Air Quality Egg").\
                    order_by(Instrument.id.asc()).all()
    dbHandler.close_session()
    # Make a list of serial numbers
    serial_numbers = [item.serial_number for item in instrument_query]
    # Fetch the data from all sensors in parallel from the AQ Egg  API
    fetcher.fetch(serial_numbers=serial_numbers)
    # Get the JSON dump
    json_dump = fetcher.get_json_dump()
    # Parser the json dump
    parser = AQEggDataParser()
    parser.parse(json_dump)

    for sensor in parser.sensors():
        datas = parser.get_sensor_data(sensor) 
        dbHandler.insert_new_aqegg_data(datas)
        print("")

    if (set(parser.sensors()) == set(serial_numbers)):
        print("All PA API calls completed!")
    
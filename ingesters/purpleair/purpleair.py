from skynet.fetcher.PurpleAirFetcher import PurpleAirFetcher
from skynet.dataparser.PurpleAirDataParser import PurpleAirDataParser
from skynet.handler.Handler import Handler
from skynet.database.config import PA_READ_KEY as READ_KEY
from skynet.database.config import GROUP_ID as group_id


if __name__=="__main__":
    # create a fetcher
    fetcher = PurpleAirFetcher(group_id=group_id, api_key=READ_KEY)
    # create a dataparser
    parser = PurpleAirDataParser()
    # create a database handler
    dbHandler = Handler()
    # fetch the data from the purpleair API
    fetcher.fetch()
    # get the json dump from the API
    json_dump = fetcher.get_json_dump()
    # parse the json dump
    parser.parse(json_dump)
    
    for sensor in parser.sensors():
        datas = parser.get_sensor_data(sensor)
        dbHandler.insert_new_purpleair_data(datas)
        print("")
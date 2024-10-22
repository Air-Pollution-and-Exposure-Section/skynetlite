from skynet.database.config import AQEGG_API_KEY as READ_KEY
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import sys


class AQEggFetcher():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = None
        self.json_dump = {}

    def get_url(self, serial_number:str):
        url = f'https://airqualityegg.com/api/v2/most-recent/messages/device/{serial_number}?apiKey={self.api_key}'
        return url
    
    def fetch(self, serial_numbers):
        urls = [(sn, self.get_url(sn)) for sn in serial_numbers]

        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            future_to_url = {executor.submit(self.fetch_data, url, sn): sn for sn, url in urls}

            for future in as_completed(future_to_url):
                try:
                    serial_number = json.loads(future.result()).get("serial_number")
                    self.json_dump[serial_number] = future.result()
                # if the API call in requests.get(url) failed
                # then skip saving the json dump
                except:
                    pass          

    def fetch_data(self, url, serial_number):
        try:
            print(f'Getting Data From -> {url} ...')
            response = requests.get(url=url)
            data = response.json()
            print(f"Success for {serial_number}!\n")
            return json.dumps(data[0] if isinstance(data, list) else data)
        except requests.RequestException as e:
            print(f"Request failed for {serial_number}: {e}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for {serial_number}")
            return None

    def get_json_dump(self):
        return self.json_dump

if __name__ == '__main__':
    pass
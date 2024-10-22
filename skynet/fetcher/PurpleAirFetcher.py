import json
import requests
from skynet.database.config import PA_READ_KEY as READ_KEY
from skynet.database.config import GROUP_ID as group_id


class PurpleAirFetcher():
    def __init__(self, group_id: int, api_key: str):
        self.group_id = group_id
        self.api_key = api_key
        self.url = self.get_url()
        self.json_dump = None

    def get_url(self):
        url = f'https://api.purpleair.com/v1/groups/{self.group_id}/members?'\
        +'&fields=last_seen%'\
        +'2C%20%20temperature_a%'\
        +'2C%20%20humidity_a%'\
        +'2C%20%20pressure_a%'\
        +'2C%20%20pm2.5_atm_a%'\
        +'2C%20%20pm2.5_cf_1_a%'\
        +'2C%20%200.3_um_count_a%'\
        +'2C%20%200.5_um_count_a%'\
        +'2C%20%201.0_um_count_a%'\
        +'2C%20%202.5_um_count_a%'\
        +'2C%20%20pm2.5_atm_b%'\
        +'2C%20%20pm2.5_cf_1_b%'\
        +'2C%20%200.3_um_count_b%'\
        +'2C%20%200.5_um_count_b%'\
        +'2C%20%201.0_um_count_b%'\
        +'2C%20%202.5_um_count_b'
        return url

    def fetch(self):
        try:
            print(f'Getting Data From -> {self.url} ...')
            headers = {'X-API-Key' : self.api_key}
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            self.json_dump = json.dumps(response.json())
            print("Success!\n")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print("Failed to parse JSON")

    def get_json_dump(self):
        return self.json_dump


if __name__=="__main__":
    pass

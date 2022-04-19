import random
import string
import json

from src.Database.Database import Database
from src.Util.CommonUtil import CommonUtil


class Register_Taxi_Services:
    list_of_taxies = []

    def __init__(self):
        config = CommonUtil.read_properties()
        self._taxi_file_path = config.get("TAXI_CSV_FILE").data
        self._collection_name = config.get("TAXI_COLLECTION").data
        self._json_file_path = config.get("AREA_BOUNDARY_JSON_PATH").data 
        self._location_data_json()
    
    def _location_data_json(self):
        with open(self._json_file_path, "r") as jsonFile:
            json_data = json.load(jsonFile)
        self._min_lat = float(json_data[0]["area_0"]["MIN_LAT_VALUE"])
        self._max_lat = float(json_data[0]["area_0"]["MAX_LAT_VALUE"])
        self._min_long = float(json_data[0]["area_0"]["MIN_LONG_VALUE"])
        self._max_long = float(json_data[0]["area_0"]["MAX_LONG_VALUE"])

    # This method will read taxi data from CSV file
    # Generates random lat-long and taxi registration plate no
    def read_data_from_csv(self):

        with open(self._taxi_file_path, 'r') as taxies:
            for taxi_data_row in taxies:
                taxi_row = taxi_data_row.rstrip()
                if taxi_row:
                    lat = random.uniform(self._min_lat, self._max_lat)
                    long = random.uniform(self._min_long, self._max_long)
                    registration_plate_no = "KA0" + str(random.randint(1, 4)) + random.choice(string.ascii_uppercase) \
                                            + str(random.randint(1000, 9999))

                    (taxi_id, taxi_type, taxi_name) = taxi_row.split(',')
                taxi_dtls = {'taxi_id': taxi_id, 'taxi_type': taxi_type, 'taxi_name': taxi_name,
                             'registration_plate_no': registration_plate_no,
                             'location': {"type": "Point", "coordinates": [long, lat]},
                             'trip_indicator': "OFF"}


                self.list_of_taxies.append(taxi_dtls)

    # This method will insert data into collection
    def insert_data_db(self):
        self._db = Database()
        taxi_ids = self._db.insert_multiple_data(self._collection_name, self.list_of_taxies)
        return taxi_ids

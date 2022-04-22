import random
import string
import json

import requests

from src.Util.CommonUtil import CommonUtil


class Taxi_Services:


    def __init__(self):
        config = CommonUtil.read_properties()
        self._taxi_file_path = config.get("TAXI_CSV_FILE").data
        self._collection_name = config.get("TAXI_COLLECTION").data
        self._register_taxi_url = config.get("REGISTER_TAXI_URL").data
        self._trip_url = config.get("TRIP_URL").data
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
    # Store data into mongodb atlas using API gateway
    def register_taxi_from_csv(self):

        with open(self._taxi_file_path, 'r',encoding='utf-8-sig') as taxies:
            for taxi_data_row in taxies:
                taxi_row = taxi_data_row.rstrip()
                if taxi_row:
                    lat = random.uniform(self._min_lat, self._max_lat)
                    long = random.uniform(self._min_long, self._max_long)
                    registration_plate_no = "KA0" + str(random.randint(1, 4)) + random.choice(string.ascii_uppercase) \
                                            + str(random.randint(1000, 9999))

                    (taxi_type, taxi_name) = taxi_row.split(',')
                taxi_dtls = {'taxi_id': registration_plate_no, 'taxi_type': taxi_type, 'taxi_name': taxi_name,
                             'location': {"type": "Point", "coordinates": [long, lat]},
                             'trip_indicator': "OFF"}

                self.call_register_taxi_api(taxi_dtls)


    # This method will call API gateway which triggers lambda function
    def call_register_taxi_api(self, taxi_data):
        taxi_data_json = json.dumps(taxi_data)
        response = requests.post(self._register_taxi_url, data=taxi_data_json)
        print("Response :", response)

    # This method will register single taxi
    def register_single_taxi(self, registration_plate, taxi_type, taxi_name):
        lat = random.uniform(self._min_lat, self._max_lat)
        long = random.uniform(self._min_long, self._max_long)
        taxi_dtls = {'taxi_id': registration_plate, 'taxi_type': taxi_type, 'taxi_name': taxi_name,
                     'location': {"type": "Point", "coordinates": [long, lat]},
                     'trip_indicator': "OFF"}
        self.call_register_taxi_api(taxi_dtls)

    # This method will start trip of taxi
    def start_trip(self, booking_data):
        booking_dtls = {}
        booking_dtls["taxi_id"] = booking_data["taxi_id"]
        booking_dtls["cust_loc"] = booking_data["cust_source_loc"]
        booking_dtls["cust_desti_loc"] = booking_data["cust_dest_loc"]
        booking_dtls["customer_id"] = booking_data["customer_id"]
        self.call_trip_api(booking_dtls)

    # This method will call API Gateway which triggers Taxi_Trip Function
    def call_trip_api(self, booking_dtls):
        response = requests.post(self._trip_url, data=json.dumps(booking_dtls))
        print("Response :", response)





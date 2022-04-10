import logging
import random
import string

from src.Util.CommonUtil import CommonUtil
from src.Util.Database import Database


class Register_Taxi_Services:
    list_of_taxies = []

    def __init__(self):
        config = CommonUtil.read_properties()
        self._taxi_file_path = config.get("TAXI_CSV_FILE").data
        self._collection_name = config.get("TAXI_COLLECTION").data
        self._max_lat = float(config.get("LAT_VALUE").data)
        self._max_long = float(config.get("LONG_VALUE").data)


    # This method will read taxi data from CSV file
    # Generates random lat-long and taxi registration plate no
    def read_data_from_csv(self):

        with open(self._taxi_file_path, 'r') as taxies:
            for taxi_data_row in taxies:
                taxi_row = taxi_data_row.rstrip()
                if taxi_row:
                    long = random.uniform(self._max_lat, self._max_long)
                    lat = random.uniform(self._max_lat, self._max_long)
                    registration_plate_no = "KA0" + str(random.randint(1, 4)) + random.choice(string.ascii_uppercase) \
                                            + str(random.randint(1000, 9999))
                    logging.info("Register_Taxi_Services | read_data_from_csv | plate no : ",registration_plate_no)
                    (taxi_id, taxi_type, taxi_name) = taxi_row.split(',')
                taxi_dtls = {'taxi_id': taxi_id, 'taxi_type': taxi_type, 'taxi_name': taxi_name,
                             "registration_plate_no": registration_plate_no,
                             'location': {"type": "Point", "coordinates": [long, lat]}}
                logging.info("Register_Taxi_Services | read_data_from_csv | taxi_dtls : ", taxi_dtls)

                self.list_of_taxies.append(taxi_dtls)

    # This method will insert data into collection
    def insert_data_db(self):
        self._db = Database()
        taxi_ids = self._db.insert_multiple_data(self._collection_name, self.list_of_taxies)
        return taxi_ids

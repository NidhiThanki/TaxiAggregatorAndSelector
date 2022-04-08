from jproperties import Properties
from pymongo import MongoClient

configs = Properties()

config_path = '../config/'

with open(config_path + 'app-config1.properties', 'rb') as read_config_file:
    configs.load(read_config_file)

host = configs.get("HOST").data
port = configs.get("PORT").data

database_name = configs.get("DB_NAME").data
taxi_data_table = configs.get("taxi_collection").data

db_handle = MongoClient(f'mongodb://{host}:{port}')

db_handle.drop_database(database_name)

taxi_db =db_handle[database_name]



with open(config_path + 'taxi_data.csv', 'r') as taxies:
    for taxi_data_row in taxies:
        taxi_row = taxi_data_row.rstrip()
        if taxi_row:
            (taxi_id, taxi_type, taxi_name, lat,long) = taxi_row.split(',')
        taxi_dtls = {'taxi_id': taxi_id, 'taxi_type': taxi_type, 'taxi_name': taxi_name, 'location': {"type": "Point", "coordinates": [lat, long]}}

        # This creates and return a pointer to the devices collection
        taxi_collection = taxi_db[taxi_data_table]

        # This inserts the data item as a document in the devices collection
        taxi_collection.insert_one(taxi_dtls)
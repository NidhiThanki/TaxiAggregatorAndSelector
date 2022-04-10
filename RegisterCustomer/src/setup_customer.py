import random
# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient

# Database host ip and port information
HOST = '127.0.0.1'
PORT = '27017'

RELATIVE_CONFIG_PATH = '../config/'

DB_NAME = 'taxi_aggregation_selection'
CUSTOMER_COLLECTION = 'customers'

# This will initiate connection to the mongodb
db_handle = MongoClient(f'mongodb://{HOST}:{PORT}')

# We drop the existing database including all the collections and data
db_handle.drop_database(DB_NAME)

# We recreate the database with the same name
taxi_aggregator_dbh = db_handle[DB_NAME]


# customer data import
# Customer document contains name (String), email (String)
# Reads customer.csv one line at a time, splits them into the data fields and inserts
with open(RELATIVE_CONFIG_PATH+CUSTOMER_COLLECTION+'.csv', 'r') as customer_fh:
    for customer_row in customer_fh:
        customer_row = customer_row.rstrip()
        if customer_row:
            (customer_id,customer_name, customer_longitude,customer_latitude) = customer_row.split(',')
            
        customer_data = {'customer_id':customer_id,'customer_name': customer_name,'customer_location':f"[{customer_longitude},{customer_latitude}]"}
        
        # This creates and return a pointer to the customers collection
        customer_collection = taxi_aggregator_dbh[CUSTOMER_COLLECTION]
        
        # This inserts the data item as a document in the customer collection
        customer_collection.insert_one(customer_data)

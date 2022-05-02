'''author :mayuri date:5/1/2022'''

import json
import base64
import pprint
from pymongo import MongoClient


def lambda_handler(event, context):
    try:
        data=event['body']
        byte_data = base64.b64decode(data)
        decode_data=json.loads(str(byte_data, 'utf-8'))    
        print(decode_data)
        # {'customer_email': 'mayuri.phanslkr@gmail.com', 'customer_type': 'General', 'old_mobile_number': 7436894200, 'new_mobile_number': 9128695537}
        new_cust_email = decode_data["new_customer_email"]
        new_cust_type = decode_data["new_customer_type"]
        current_mobile_number = decode_data["current_mobile_number"]
        new_mobile_number = decode_data["new_mobile_number"]
        #Access the MongoDB Service
        db_uri="mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        aggregator_cli = MongoClient(db_uri)
        # Create a Database
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        # Create Collection
        customers = aggregator_db['customer_registration_data']
        # Updating items
        filter1 = {'mobile_number': current_mobile_number}
        # Values to be updated.
        # {'new_customer_email': None, 'new_customer_type': 'Premium', 'current_mobile_number': 8904034044, 'new_mobile_number': 7499089251
        if new_cust_email != None and new_cust_type != None and new_mobile_number != None:
            updt_val = {"$set": {'customer_email': new_cust_email,'customer_type': new_cust_type,'mobile_number': new_mobile_number}}
        elif new_cust_type != None and new_cust_email != None:
            updt_val = {"$set": {'customer_type': new_cust_type,'customer_email': new_cust_email}}
        elif new_mobile_number != None and new_cust_type != None:
            updt_val = {"$set": {'mobile_number': new_mobile_number,'customer_type': new_cust_type}}
        elif new_mobile_number != None and  new_cust_email != None:
            updt_val = {"$set": {'mobile_number': new_mobile_number,'customer_email': new_cust_email}}
        elif new_cust_email != None and new_cust_type == None and new_mobile_number == None:
            updt_val = {"$set": {'customer_email': new_cust_email}}
        elif new_cust_email == None and new_cust_type != None and new_mobile_number == None:
            updt_val = {"$set": {'customer_type': new_cust_type}}
        elif new_cust_email == None and new_cust_type ==None and new_mobile_number != None:
            updt_val = {"$set": {'mobile_number': new_mobile_number}}
        else:
            print("Nothing to update!")
            return -1
        customers.update_one(filter1, updt_val)
        return 1
    except Exception as e:
        print("eror")
        pprint.pprint(str(e))
        return -1
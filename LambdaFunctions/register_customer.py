'''author :mayuri date:4/16/2022'''

import email
import boto3
import json
import base64
from pymongo import MongoClient
import pprint


def lambda_handler(event, context):
    try:
        res = -1
        data=event['body']
        byte_data = base64.b64decode(data)
        decode_data=json.loads(str(byte_data, 'utf-8'))    
        print(decode_data)
        #Access the MongoDB Service
        db_uri="mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        aggregator_cli = MongoClient(db_uri)
        # Create a Database
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        # Create Collection
        customers = aggregator_db['customer_registration_data']
        
        # Populate the Collections
        reg_res = customers.insert_many(decode_data)
        print("register: ",reg_res)
        if reg_res:
            for decode_data in decode_data:
                customer_id = decode_data["customer_id"]
                email_id=decode_data["customer_email"]
                timestamp=decode_data["timestamp"]
                customer_type=decode_data["customer_type"]
            customer_name = decode_data["customer_first_name"] + " " + decode_data["customer_last_name"]
            msg = f"Customer: {customer_name} of user type: {customer_type} is successfully registerd with customer id: {customer_id} on date: {timestamp} for receiving cab services "
            res = 1
            dict_msg = {"res": res, "msg": msg, "email_id": email_id, "status":"Registration Status"}
            aggregator_cli.close()
            return dict_msg
           
    except Exception as e:
        pprint.pprint(str(e))
        aggregator_cli.close()
        return {"res":-1}
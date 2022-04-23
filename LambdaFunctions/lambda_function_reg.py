'''author :mayuri date:4/16/2022'''

import email
import boto3
import json
import base64
from pymongo import MongoClient


def lambda_handler(event, context):
    try:
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
        # res = customers.delete_many({})
        
        # Populate the Collections
        res = customers.insert_many(decode_data)
        
        if res:
            for decode_data in decode_data:
                customer_id = decode_data["customer_id"]
                email_id=decode_data["customer_email"]
                timestamp=decode_data["timestamp"]
                customer_type=decode_data["customer_type"]
            customer_name = decode_data["customer_first_name"] + " " + decode_data["customer_last_name"]
            msg = f"Customer: {customer_name} of user type: {customer_type} is successfully registerd with customer id: {customer_id} on date: {timestamp} for receiving cab services "
            try:
                ses_client = boto3.client("ses", region_name="us-east-1") 
                CHARSET = "UTF-8"
                response = ses_client.send_email(
                    Destination={
                        "ToAddresses": [
                            email_id
                        ],
                    },
                    Message={
                        "Body": {
                            "Text": {
                                "Charset": CHARSET,
                                "Data": msg,
                            }
                        },
                        "Subject": {
                            "Charset": CHARSET,
                            "Data": "Registration Status",
                        },
                    },
                    Source=email_id,
                    )
            except Exception as e:
                print(str(e))
                return 1
            return 1
    except Exception as e:
        print(str(e))
        return -1
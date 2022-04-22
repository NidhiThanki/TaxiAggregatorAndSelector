import json
import base64

from pymongo import MongoClient


def lambda_handler(event, context):
    taxi_data = event['body']
    payload = base64.b64decode(taxi_data)
    payload = str(payload, 'utf-8')

    payload_rec = json.loads(payload)
    print("payload_rec ", payload_rec)
    db_uri = "mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
    db_conn = MongoClient(db_uri)
    db_name = db_conn['taxi_aggregation_selection']
    taxi_collection = db_name['taxi_registration_data']
    res = taxi_collection.insert_one(payload_rec)

    print("Result :", res.inserted_id)

    response_obj = {"statusCode": 200, "Registration": "Completed"}

    return json.loads(json.dumps(response_obj, default=str))

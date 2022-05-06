import json


from pymongo import MongoClient

def lambda_handler(event, context):

    taxi_id = event["queryStringParameters"]["taxi_id"]

    db_uri = "mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
    db_conn = MongoClient(db_uri)
    db_name = db_conn['taxi_aggregation_selection']
    taxi_collection = db_name['taxi_registration_data']
    key = {"taxi_id": taxi_id}
    result = taxi_collection.find_one(key)
    db_conn.close()
    return json.loads(json.dumps(result, default=str))

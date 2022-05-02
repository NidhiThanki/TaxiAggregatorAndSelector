'''author :aaron date:4/20/2022'''


from pymongo import MongoClient
import pprint
import datetime

def lambda_handler(event,context):
    try:
        db_uri="mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        aggregator_cli = MongoClient(db_uri)
        
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        taxi_location_updates = aggregator_db['taxi_location_update_data']
        taxi_registration_data = aggregator_db['taxi_registration_data']
        
        taxi_loc_updates=[]

        # Get the last 1 hour data
        start = str(datetime.datetime.now() - datetime.timedelta(minutes=1))
        # start = str(datetime.datetime.now() - datetime.timedelta(seconds=30))
        # start = str(datetime.datetime.now() - datetime.timedelta(hours=60))
        end = str(datetime.datetime.now())

        for locationUpdateRecord in taxi_location_updates.find({'timestamp': {'$gte': start, '$lt': end}}):
            locationUpdateRecord.pop('_id')
            taxi_loc_updates.append(locationUpdateRecord)
        for locationUpdateRecord in taxi_registration_data.find({'trip_indicator': 'OFF'}):
            locationUpdateRecord.pop('_id')
            taxi_loc_updates.append(locationUpdateRecord)
        if len(taxi_loc_updates) > 0:
            return taxi_loc_updates
        return 1
    except Exception as e:
        pprint.pprint(str(e))
        return -1
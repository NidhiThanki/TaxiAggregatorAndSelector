'''author :mayuri date:4/16/2022'''

from pprint import pprint
from symtable import Function
from pymongo import MongoClient, GEOSPHERE
import pprint
import json
import boto3
import datetime
from bson.son import SON
import geopy
from geopy.distance import geodesic
import time
import random
import string


def lambda_handler(event, context):
    try:
        booking_req = None
        book_data =None
        nearest_taxi_details = None
        res = -1
        cust_data = event['queryStringParameters']
        print(cust_data)
        cust_source_loc = {"coordinates": [float(cust_data["source_long"]), float(cust_data["source_lat"])],
                           "type": cust_data["type"]}
        _timestamp = cust_data['timestamp']
        customer_id = cust_data['customer_id']
        customer_type = cust_data["customer_type"]
        book_type =cust_data["book_type"]
        taxi_type = cust_data['taxi_type']
        email_id = cust_data["email_id"]
        customer_name = cust_data["customer_first_name"] + " " + cust_data["customer_last_name"]
        cust_dest_loc = {"coordinates": [float(cust_data["dest_long"]), float(cust_data["dest_lat"])],
                         "type": cust_data["type"]}
        db_uri = "mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        # Access the MongoDB Service
        aggregator_cli = MongoClient(db_uri)
        # Database
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        booking = aggregator_db['booking_data']
        customers = aggregator_db['customer_registration_data']
        customer_ind = customers.find_one({"customer_id": customer_id}, {"_id": 0, "trip_indicator": 1})

        booking_id = "Book_" + str(random.randint(100, 999)) + str(random.choice(string.ascii_letters)) + \
                     str(random.randint(10000, 99999))

        if customer_ind["trip_indicator"] == "ON":
            if customer_type.lower() == "premium":
                book_req = 1
            else:
                book_req = -1
                comment = "Customer not premium member, not allowed to book taxi while in trip "
                res = 0
        else:
            book_req = 1
        if book_req == 1:
            taxis = aggregator_db['taxi_registration_data']
            # Create Index(es)
            taxis.create_index([('location', GEOSPHERE)])
            customers.create_index([('location', GEOSPHERE)])
            # checking if taxis available within 10km from customer's location
            taxi_in_range = []
            srclong = cust_source_loc["coordinates"][0]
            srclat = cust_source_loc["coordinates"][1]
            # print(srclong,srclat)
            start = geopy.Point(srclat, srclong)
            # Query: taxis for  customer within 10km and required taxi type
            range_taxi_type_query = {'location': SON([("$near", cust_source_loc), ("$maxDistance", 10000)]),
                           'trip_indicator': {"$ne": "ON"},'taxi_type': {"$eq": taxi_type}}
           # Query: taxis for  customer within 10km and default taxi type
            range_default_taxi_type_query = {'location': SON([("$near", cust_source_loc), ("$maxDistance", 10000)]),
                           'trip_indicator': {"$ne": "ON"}}
            # Query: taxis for  customer within 10km
            range_query = {'location': SON([("$near", cust_source_loc), ("$maxDistance", 10000)]),
                           'trip_indicator': {"$ne": "ON"}}
            # Query: avaialble taxis for  customer 
            nearest_query = {'location': {"$near": cust_source_loc}, 'trip_indicator': {"$ne": "ON"}}
            if taxi_type.lower() == "all":
                query = range_default_taxi_type_query
            else:
                query = range_taxi_type_query
            # Getting taxis for  customer within 10km and required/default taxi type
            for doc in taxis.find(query).limit(1):
                doc.pop('_id')
                nearest_taxi_details = doc
            if nearest_taxi_details:
                res = 1
                end = geopy.Point(doc['location']['coordinates'][1], doc['location']['coordinates'][0])
                dist_dict = {"distance_km": geodesic(start, end).km}
                print(doc)
                booking_status = "Successful"
                comment = "Success"
                taxi_id = nearest_taxi_details['taxi_id']

            else:
                booking_status = "Failure"
                taxi_id = "None"
                comment = "No taxis available within 10km range from customer with required taxi type.Sending other taxi options to customer!"
                # Getting taxis for  customer within 10km
                for doc in taxis.find(range_query).limit(1):
                    doc.pop('_id')
                    nearest_taxi_details = doc
                if nearest_taxi_details:
                    taxi_id = nearest_taxi_details['taxi_id']
                    end = geopy.Point(doc['location']['coordinates'][1], doc['location']['coordinates'][0])
                    dist_dict = {"distance_km": geodesic(start, end).km}

                    print(doc)
                else:
                    comment = "No taxis available within 10km range from customer.Sending other taxi options to customer!"
                    # Getting available taxis for  customer 
                    for doc in taxis.find(nearest_query).limit(1):
                        doc.pop('_id')
                        nearest_taxi_details = doc
                    if nearest_taxi_details:
                        taxi_id = nearest_taxi_details['taxi_id']
                        end = geopy.Point(doc['location']['coordinates'][1], doc['location']['coordinates'][0])
                        dist_dict = {"distance_km": geodesic(start, end).km}
                        print(doc)
                    else:
                        comment = "Sorry, No taxis available !!"
            if nearest_taxi_details:
                book_data = {**dist_dict, **nearest_taxi_details}
                if res == 1:
                    # Updating trip indicator for nearest taxi.
                    filter1 = {'taxi_id': taxi_id}
                    # Values to be updated.
                    taxi_ind = {"$set": {'trip_indicator': "ON"}}
                    taxis.update_one(filter1, taxi_ind)
                    # Updating trip indicator and source location as per trip for customer.
                    filter2 = {'customer_id': customer_id}
                    # Values to be updated.
                    cust_ind = {"$set": {'trip_indicator': "ON"}}
                    cust_src_loc = {"$set": {'location': cust_source_loc}}
                    customers.update_one(filter2, cust_ind)
                    customers.update_one(filter2, cust_src_loc)
                    # since already updated trip_indicator in DB, updating nearest taxi details here
                    nearest_taxi_details["trip_indicator"] = "ON"
                    booking_req = {"timestamp": _timestamp, "customer_id": customer_id, "customer_type": customer_type,
                                   "taxi_id": taxi_id, "cust_source_loc": cust_source_loc,
                                   "cust_dest_loc": cust_dest_loc, "distance_km": dist_dict["distance_km"],
                                   "booking_status": booking_status, "trip_indicator": "In-progress",
                                   "comment": comment, "booking_id": booking_id,"book_type":book_type, "customer_name": customer_name}
                    # copying booked details and removing/adding required fields for trip start
                    booking_details = booking_req.copy()
                    [booking_details.pop(key) for key in ["timestamp", "taxi_id", "booking_status", "comment"]]
                    # unpacking dicts for:  trip start request details
                    booking_details = {**book_data, **booking_details}
                    msg = f"Customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} is successfully booked on date: {_timestamp}. These are the details : {booking_details}"
                else:
                    booking_req = {"timestamp": _timestamp, "customer_id": customer_id, "customer_type": customer_type,
                                   "taxi_id": "None", "cust_source_loc": cust_source_loc, " cust_dest_loc": cust_dest_loc,
                                   "booking_status": booking_status, "trip_indictor": "OFF", "comment": comment,"booking_id": booking_id,"book_type":book_type}
                    if book_data != None:
                        booking_details = booking_req.copy()
                        [booking_details.pop(key) for key in ["timestamp", "taxi_id", "booking_status", "comment"]]
                        msg = f"Booking Failed for customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} on date: {_timestamp}.These are the details : {comment}.Here are available taxi options : {book_data}"
                    else:
                        msg = f"Booking Failed for customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} on date: {_timestamp}.These are the details : {comment}."
            else:
                return {"res": -1}
            print("Booking Request to insert data:", booking_req)
            print("Booking Details for trip start:" ,booking_details)
            print("MSG: ",msg)
            # Populating booking data collection
            if booking_req:
                booking.insert_one(booking_req)
                print("Data inserted in booking table! ")
                dict_msg = {"res": res, "msg": msg, "email_id": email_id,"status":"Booking Status"}
                if res == 1:
                    booking_details = {**dict_msg, **booking_details}
                else:
                    booking_details = dict_msg
            print("Booking details : ", booking_details)
            return booking_details
        return {"res":res}
    except Exception as e:
        print("exception")
        pprint.pprint(str(e))
        return {"res": -1}
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


def lambda_handler(event,context):
    try:
        booking_req = None
        nearest_taxi_details = None
        res = -1
        cust_data=event['queryStringParameters']        
        print(cust_data)           
        cust_source_loc = {"coordinates":[float(cust_data["source_long"]),float(cust_data["source_lat"])],"type":cust_data["type"]}
        _timestamp = cust_data['timestamp']
        customer_id=cust_data['customer_id']  
        customer_type=cust_data["customer_type"]
        taxi_type = cust_data['taxi_type']
        email_id = cust_data["email_id"]
        customer_name = cust_data["customer_first_name"] + " " + cust_data["customer_last_name"]
        cust_dest_loc = {"coordinates":[float(cust_data["dest_long"]),float(cust_data["dest_lat"])],"type":cust_data["type"]}       
        db_uri="mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        #Access the MongoDB Service
        aggregator_cli = MongoClient(db_uri)
        # Database
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        booking = aggregator_db['booking_data']
        customers = aggregator_db['customer_registration_data']
        customer_ind = customers.find_one({"customer_id":customer_id},{"_id":0,"trip_indicator":1})
        
        if customer_ind["trip_indicator"] == "ON":   
            if customer_type.lower() == "premium":
                book_req = 1
            else:
                book_req =-1
                comment = "Customer not premium member, not allowed to book taxi while in trip "
                res = -1
        else:
            book_req = 1
        if book_req == 1:
            taxis = aggregator_db['taxi_registration_data']
            # Create Index(es)
            taxis.create_index([('location', GEOSPHERE)])
            customers.create_index([('location', GEOSPHERE)])
            # checking if taxis available within 10km from customer's location
            taxi_in_range = []
            srclong =cust_source_loc["coordinates"][0]
            srclat =cust_source_loc["coordinates"][1]
            # print(srclong,srclat)
            start = geopy.Point(srclat, srclong)
            # Getting taxis within a certain 10km range from a customer
            range_query = {'location': SON([("$near", cust_source_loc), ("$maxDistance", 10000)]),'trip_indicator': {"$ne": "ON"}}
            for doc in taxis.find(range_query):
                doc.pop('_id')
                taxi_in_range.append(doc["taxi_id"])  
                end = geopy.Point(doc['location']['coordinates'][1], doc['location']['coordinates'][0])
                # print("total distance " + str(geodesic(start, end)))
            # print(taxi_in_range)
            if len(taxi_in_range) >0:
                # Getting the nearest taxis to a customer
                print('######################## THE NEAREST TAXI ########################')
                if taxi_type.lower() == "all":
                    nearest_query = {'location': {"$near": cust_source_loc},'trip_indicator': {"$ne": "ON"}}
                else:
                    nearest_query = {'location': {"$near": cust_source_loc},'trip_indicator': {"$ne": "ON"},'taxi_type':{"$eq":taxi_type}}
                for doc in taxis.find(nearest_query).limit(1):
                    doc.pop('_id')
                    nearest_taxi_details = doc
                    # calculating distance
                    end = geopy.Point(doc['location']['coordinates'][1], doc['location']['coordinates'][0])
                    dist_dict = {"distance_km":geodesic(start, end).km}
                    print(doc)
                if nearest_taxi_details:
                    booking_status = "Successful"
                    comment= "Success"
                    taxi_id = nearest_taxi_details['taxi_id']
                    # Updating trip indicator for nearest taxi.
                    filter1 = { 'taxi_id': taxi_id } 
                    # Values to be updated.
                    taxi_ind = { "$set": {'trip_indicator': "ON"}}
                    taxis.update_one(filter1, taxi_ind)
                    # Updating trip indicator and source location as per trip for customer.
                    filter2 = { 'customer_id': customer_id } 
                    # Values to be updated.
                    cust_ind = { "$set": {'trip_indicator': "ON"}}
                    cust_src_loc ={"$set": {'location': cust_source_loc}}
                    customers.update_one(filter2, cust_ind)
                    customers.update_one(filter2, cust_src_loc)
                    # since already updated trip_indicator in DB, updating nearest taxi details here 
                    nearest_taxi_details["trip_indicator"] = "ON"
                    booking_req = {"timestamp":_timestamp,"customer_id":customer_id,"customer_type":customer_type,"taxi_id":taxi_id,"cust_source_loc":cust_source_loc," cust_dest_loc":cust_dest_loc,"distance_km":dist_dict["distance_km"],"booking_status":booking_status,"trip_indicator":"In-progress","comment":comment}
                    # copying booked details and removing/adding required fields for trip start
                    booking_details = booking_req.copy()
                    [booking_details.pop(key) for key in ["timestamp","taxi_id","booking_status","comment"]]
                    # unpacking dicts for:  trip start request details
                    booking_details = {**dist_dict,**nearest_taxi_details,**booking_details}                
                    msg = f"Customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} is successfully booked on date: {_timestamp}. These are the details : {booking_details}"
                    res = 1
                else:
                    booking_status = "Failure"
                    taxi_id = "None"
                    comment = "Taxi type selected by customer not available! "
                    booking_req = {"timestamp":_timestamp,"customer_id":customer_id,"customer_type":customer_type,"taxi_id":taxi_id,"cust_source_loc":cust_source_loc," cust_dest_loc":cust_dest_loc,"booking_status":booking_status,"trip_indictor":"OFF","comment":comment}
                    msg = f"Booking Failed for customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} on date: {_timestamp}. These are the details : {comment}"
            else:
                booking_status = "Failure"
                taxi_id = "None" 
                comment = "No taxis available within 10km range from customer!"
                booking_req = {"timestamp":_timestamp,"customer_id":customer_id,"customer_type":customer_type,"taxi_id":taxi_id,"cust_source_loc":cust_source_loc," cust_dest_loc":cust_dest_loc,"booking_status":booking_status,"trip_indictor":"OFF","comment":comment} 
                msg = f"Booking Failed for customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} on date: {_timestamp}. These are the details : {comment}" 
        else:
            booking_status = "Failure"
            taxi_id = "None" 
            booking_req = {"timestamp":_timestamp,"customer_id":customer_id,"customer_type":customer_type,"taxi_id":taxi_id,"cust_source_loc":cust_source_loc," cust_dest_loc":cust_dest_loc,"booking_status":booking_status,"trip_indictor":"OFF","comment":comment}
            msg = f"Booking Failed for customer: {customer_name} of user type: {customer_type} with customer id: {customer_id} on date: {_timestamp}. These are the details : {comment}"  
        print("Booking Request to insert data:" ,booking_req)
        # print("Booking Details for trip start:" ,booking_details)
        # Populating booking data collection
        if booking_req:
            booking.insert_one(booking_req)
            print("Data inserted in booking table!")
            dict_msg = {"res":res,"msg":msg,"email_id": email_id}
            if res == 1:
                booking_details = {**dict_msg,**booking_details}
            else:
                booking_details = dict_msg
        return booking_details
    except Exception as e:
        print("exception")
        pprint.pprint(str(e))
        return {"res":-1}
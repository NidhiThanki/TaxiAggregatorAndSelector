import base64
import json
import math

import geopy as geopy
from geopy.distance import lonlat, geodesic
import numpy as np
from time import time, sleep
import datetime
from datetime import timedelta

from pymongo import MongoClient


def lambda_handler(event, context):
    taxi_data = event['body']
    # taxi_data = event['detail']['fullDocument']
    payload = base64.b64decode(taxi_data)
    payload = str(payload, 'utf-8')

    payload_rec = json.loads(payload)
    print("payload_rec ", payload_rec)
    db_uri = "mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"

    db_conn = MongoClient(db_uri)
    db_name = db_conn['taxi_aggregation_selection']
    location_collection = db_name['taxi_location_update_data']
    taxi_collection = db_name["taxi_registration_data"]
    customer_collection = db_name["customer_registration_data"]
    booking_collection = db_name["booking_data"]

    start = geopy.Point(payload_rec["cust_loc"]["coordinates"][1],
                        payload_rec["cust_loc"]["coordinates"][0])
    end = geopy.Point(payload_rec["cust_desti_loc"]["coordinates"][1],
                      payload_rec["cust_desti_loc"]["coordinates"][0])
    list_of_points = points_between(start, end, 5, False)

    time_inc = 0
    for idx in range(0, len(list_of_points[1])):
        current_time = datetime.datetime.now()
        time_for_simulation = current_time + timedelta(minutes=time_inc)
        location_update_data = {
            "taxi_id": payload_rec["taxi_id"],
            "booking_id": payload_rec["booking_id"],
            "timestamp": str(time_for_simulation),
            "location": {"type": "Point",
                         "coordinates": [list_of_points[2][idx], list_of_points[1][idx]]},
            "customer_id": payload_rec["customer_id"]
        }
        res = location_collection.insert_one(location_update_data)
        time_inc += 1
        print("Result after insert_one :", res.inserted_id)

    # update trip_indicator in  customer_collection
    key_of_customer = {"customer_id": payload_rec["customer_id"]}
    customer_data = {"$set": {"trip_indicator": "OFF"}}
    res = customer_collection.update_one(key_of_customer, customer_data)
    print("Result after customer update_one :", res.matched_count)

    # update trip_indicator and location of taxi in Register_taxi collection
    dest_long = payload_rec["cust_desti_loc"]["coordinates"][0]
    dest_lat = payload_rec["cust_desti_loc"]["coordinates"][1]
    key_of_taxi = {"taxi_id": payload_rec["taxi_id"]}
    latest_taxi_data = {
        "$set": {"trip_indicator": "OFF", "location": {"type": "Point", "coordinates": [dest_long, dest_lat]}}}
    res = taxi_collection.update_one(key_of_taxi, latest_taxi_data)
    print("Result after taxi's update_one :", res.matched_count)

    # update trip_indicator in booking collection
    key_booking = {"booking_id":payload_rec["booking_id"]}
    updated_fields = {"$set": {"trip_indicator": "Complete"}}
    res = booking_collection.update_one(key_booking,updated_fields)
    print("Result after updating booking fields : ", res.matched_count)

    response_obj = {"statusCode": 200, "Simmulation": "Completed for taxi " + payload_rec["taxi_id"]}

    return response_obj


# returns lists of latitude, longitude, area covered and bearing points
def points_between(start, end, numpoints, constantvalue=False):
    distance = []
    latitude = []
    longitude = []

    lat0 = start.latitude
    lon0 = start.longitude
    lat1 = end.latitude
    lon1 = end.longitude

    if constantvalue and np.isclose(lat0, lat1):
        latitude = np.ones(numpoints) * lat0
        longitude = np.linspace(lon0, lon1, num=numpoints)
        for lon in longitude:
            distance.append(geodesic(start, geopy.Point(lat0, lon)).km)
        if lon1 > lon0:
            b = 90
        else:
            b = -90
    elif constantvalue and np.isclose(lon0, lon1):
        latitude = np.linspace(lat0, lat1, num=numpoints)
        longitude = np.ones(numpoints) * lon0
        for lat in latitude:
            distance.append(geodesic(start, geopy.Point(lat, lon0)).km)
            if lat1 > lat0:
                b = 0
            else:
                b = 180
    else:
        total_distance = geodesic(start, end).km
        distance = np.linspace(0, total_distance, num=numpoints)
        b = bearing(lat0, lon0, lat1, lon1)

        for d in distance:
            p = geodesic().destination(start, b, d)
            latitude.append(p.latitude)
            longitude.append(p.longitude)

    return list(map(np.array, [distance, latitude, longitude, b]))


def bearing(lat0, lon0, lat1, lon1):
    lat0_rad = np.radians(lat0)
    lat1_rad = np.radians(lat1)
    diff_rad = np.radians(lon1 - lon0)
    x = np.cos(lat1_rad) * np.sin(diff_rad)
    y = np.cos(lat0_rad) * np.sin(lat1_rad) - np.sin(
        lat0_rad) * np.cos(lat1_rad) * np.cos(diff_rad)
    b = np.arctan2(x, y)
    return np.degrees(b)

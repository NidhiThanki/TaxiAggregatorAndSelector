'''author :mayuri date:4/16/2022'''


# Imports ObjectId to convert to the correct format before querying in the db
from asyncore import read
from random import randint
import random,json
import datetime
import requests
from src.Util.CommonUtil import CommonUtil
from src.Taxi.taxi_services import Taxi_Services

# customer document contains customer_name (String), email (String), and role (String) fields
class Customer_Services():
    customer_data_list = []

    def __init__(self):
        config = CommonUtil.read_properties()
        self._customer_file_path = config.get("CUSTOMER_CSV_FILE").data
        self._collection_name = config.get("CUSTOMER_COLLECTION").data
        self._json_file_path = config.get("AREA_BOUNDARY_JSON_PATH").data
        self.post_url = config.get("POST_URL").data   
        self.get_url = config.get("GET_URL").data 
        self.book_url = config.get("BOOK_URL").data 
        self.email_url = config.get("EMAIL_URL").data
        self.updt_url = config.get("UPDT_URL").data
        self._location_data_json()
    
    def _location_data_json(self):
        with open(self._json_file_path, "r") as jsonFile:
            json_data = json.load(jsonFile)
        self._min_lat = float(json_data[0]["area_0"]["MIN_LAT_VALUE"])
        self._max_lat = float(json_data[0]["area_0"]["MAX_LAT_VALUE"])
        self._min_long = float(json_data[0]["area_0"]["MIN_LONG_VALUE"])
        self._max_long = float(json_data[0]["area_0"]["MAX_LONG_VALUE"])

    # Reads customer.csv one line at a time, splits them into the data fields and inserts
    def read_data_from_csv(self):
        customer_data_list = []
        with open(self._customer_file_path, 'r') as customer_fh:
            for customer_row in customer_fh:
                customer_row = customer_row.rstrip()
                if customer_row:
                    (customer_first_name, customer_last_name,customer_type,customer_email,trip_indicator,mobile_number) = customer_row.split(',')                            
                customer_data = {"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"customer_email":customer_email,"customer_type":customer_type,"trip_indicator":trip_indicator,"mobile_number":mobile_number}
                customer_data_list.append(customer_data)
            return customer_data_list
            
    # generate uniques customer id 
    def generate_customer_id(self,cust_first,cust_last):
        start = randint(1,10)
        end = randint(11,20)
        rand_num = randint(start,end)
        cust_name = cust_first[:4]+cust_last[:2]
        cust_id = f"{cust_name}_{rand_num}"        
        return cust_id

    # •	Service area validation: check for area boundary
    def check_location(self,lat,long):
        if self._min_lat <=  lat <= self._max_lat  and  self._min_long <=  long <= self._max_long:
            return 1
        return -1
        
    # register one customer
    def register_one(self,customer_first_name,customer_last_name,customer_email,customer_type,lat,long,mobile_number):
        try:
            # check location cordinates
            loc_res = self.check_location(lat,long)
            if loc_res != -1:
                # read customer customer details
                res = self.get_customer_details(mobile_number)
                cust_res = json.loads(res)
                # print(cust_res)
                if cust_res == -1:                          
                    customer_id = self.generate_customer_id(customer_first_name,customer_last_name)
                    _timestamp=datetime.datetime.now()
                    customer_data = {"timestamp":str(_timestamp),"customer_id":customer_id,"customer_type":customer_type,"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"customer_email":customer_email,"trip_indicator":"OFF","mobile_number":mobile_number,"location":{"type":"Point","coordinates":[long,lat]}}        
                    reg_res = self.register_connection([customer_data]) 
                    if reg_res["res"] != -1:
                        self.send_email_to_customer(reg_res)
                        print(f"==================Registration Successful for customer: {customer_first_name} {customer_last_name}==================")            
                else:
                    print("============Customer already registered!! ====================")
            else:
                print("===========Sorry, Cab service is not provided at this location!=============")
        except Exception as e:
            print("RegisterOneError:",str(e))

    # Customer simulation: registers many customer from list/csv files
    def register_many(self):
        try:
            customer_data = self.read_data_from_csv()
            for val in customer_data:
                customer_id = self.generate_customer_id(val['customer_first_name'],val['customer_last_name'])
                _timestamp=datetime.datetime.now()
                long = random.uniform(self._min_long, self._max_long)
                lat = random.uniform(self._min_lat, self._max_lat)
                val["timestamp"] = str(_timestamp)
                val["customer_id"]=customer_id
                val["location"]={"type":"Point","coordinates":[long,lat]}
                self.customer_data_list.append(val)
            self.register_connection(self.customer_data_list)
        except Exception as e:
            print("RegisterManyError:",str(e))        

    # connect to API gateway for registration
    def register_connection(self,cust_data):
        #creaating json data
        customer_data = json.dumps(cust_data)
        # connecting to endpoint to send data
        res = requests.post(self.post_url,data=customer_data)
        reg_res = json.loads(res.text)
        if reg_res["res"] != -1:
            print("==================Connected to Register API==================")
            return reg_res
        else:
            print("Check status!")
            return {"res":-1}

    # update customer details
    def updt_customer_data(self,new_customer_email,new_customer_type,current_mobile_number,new_mobile_number):
        # read customer customer details
        res = self.get_customer_details(current_mobile_number)
        cust_res = json.loads(res)
        # print(cust_res)
        if cust_res != -1:          
            cust_data = {"new_customer_email":new_customer_email,"new_customer_type":new_customer_type,"current_mobile_number":current_mobile_number,"new_mobile_number":new_mobile_number}
            customer_data = json.dumps(cust_data)
            # connecting to endpoint to update data
            res = requests.put(self.updt_url,data=customer_data)
            print("==================Connected to Update API==================")
            updt_res = json.loads(res.text)
            if updt_res == 1:
                print("==================Data Updated Successfully! ==================")
                if new_customer_email != None:
                    email_id = new_customer_email
                else:
                    email_id = cust_data["email_id"]
                status ="Update Status"
                msg = "Customer data is sucessfully updated!"
                updt_data = {"res" : 1, "email_id":email_id,"status":status,"msg":msg}
                self.send_email_to_customer(updt_data)
                return updt_res
            else:
                print("Check status!")
                return -1
        else:
            print("===========Customer is not registered! ============")


    # connect to API gateway to read customer details
    def get_customer_details(self,mobile_number):
        try:
            data_req = {"req":"one","mobile_number": mobile_number}
            # connecting to endpoint to send data
            response = requests.get(self.get_url,params = data_req)            
            return response.text
        except:
            return -1
    
    # get data for all customer
    def get_registered_customers(self):
        try:
            data_req = {"req":"all"}
            # connecting to endpoint to send data
            response = requests.get(self.get_url,params = data_req)            
            return response.text
        except:
            return -1

    # Booking and proximity search : raise booking request and return nearest taxi via API
    def booking(self,customer_first_name,customer_last_name,source_lat,source_long,dest_lat,dest_long,taxi_type,mobile_number,book_type):
        # check if source/destination location is in service area boundary
        source_res= self.check_location(source_lat,source_long)
        dest_res = self.check_location(dest_lat,dest_long)
        if source_res != -1 and dest_res != -1:
            try:
                # read customer customer details           
                res = self.get_customer_details(mobile_number)
            except Exception as e:
                print(str(e))         
            read_res = json.loads(res)
            if read_res != -1:
                # check if customer is "Non-premium" and  already in trip
                cust_trip_ind = read_res["trip_indicator"]
                cust_type = read_res["customer_type"] 
                # connecting to endpoint to send data
                cust_id = read_res["customer_id"]
                cust_email = read_res["customer_email"]
                _timestamp=datetime.datetime.now()
                customer_type = read_res["customer_type"]
                # registered customer who is booking trip either for "self" or "other" customer
                booking_customer_name = read_res["customer_first_name"] + " " + read_res["customer_last_name"]
                cust_data = {"timestamp":str(_timestamp),"customer_id": cust_id,"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"email_id":cust_email,"customer_type":customer_type,"source_lat":source_lat,"source_long":source_long,"type":"Point","taxi_type":taxi_type,"dest_lat":dest_lat,"dest_long":dest_long,"book_type":book_type}           
                if book_type.lower() == "self":                    
                    response = requests.get(self.book_url,params = cust_data)
                else:
                    # premium members can book taxi for other customers
                    if cust_type.lower() == "premium":
                        cust_data = {"timestamp":str(_timestamp),"customer_id": cust_id,"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"email_id":cust_email,"customer_type":"Other","source_lat":source_lat,"source_long":source_long,"type":"Point","taxi_type":taxi_type,"dest_lat":dest_lat,"dest_long":dest_long,"book_type":book_type}
                        '''============Booking taxi for unregistered/third party customer============'''
                        response = requests.get(self.book_url,params = cust_data)
                    else:
                        if cust_trip_ind == "ON":
                            print(f"Customer: {booking_customer_name} is not premium type user.Sorry,not allowed to book taxi while already in trip!!")
                        else:
                            print(f"Customer: {booking_customer_name} is premium type user.Sorry,not allowed to book taxi for unregistered/third party customers!!")
                        return -1
                book_res = json.loads(response.text)
                # print(book_res)
                customer_name = customer_first_name + " " + customer_last_name
                try:
                    if book_res["message"] == "Internal Server Error":
                        print(f"=========Booking Unsuccessful for customer : {customer_name}!!===========")
                        return -1
                except:
                    if book_res["res"] == "exception":
                        print(f"=========Booking Unsuccessful for customer : {customer_name}!!===========")
                        return -1                   
                    else :
                        self.send_email_to_customer(book_res)
                   
                if book_res["res"] != -1 :
                    print("=========Connected to Booking API Endpoint==========")
                    print(f"=========Booking Successful for customer : {customer_name}!!===========")
                    self.send_email_to_driver(book_res)
                    book_res.pop("msg")
                    book_res.pop("email_id")
                    book_res.pop("res")
                    self.customer_trip(book_res)
                    return book_res
                elif book_res["res"] == -1:
                    # print(book_res)
                    print(f"=========Check status in booking table for customer: {customer_name}===========")
                    return -1
                elif book_res["res"] == 0:
                    print("===========Customer not allowed for booking services! ============")
                else:
                    print("===Faiulre!!===")
                    return -1
            else:
                print("===========Customer not registered for services! ============")
                return 0
        else:
            print("==========Sorry,cab service is not available in source/destination area!=========") 

    # notification to driver
    def send_email_to_driver(self, booking_data):
        email_data = {}
        email_data["email_id"] = booking_data["driver_email_id"]
        email_data["status"] = "Taxi booked with booking id " + booking_data["booking_id"]
        msg = "Your taxi has been booked by " + booking_data["customer_name"]
        distance = " Total distance : " + str(booking_data["distance_km"])
        source_location = " Source location is :" + str(booking_data["cust_source_loc"]["coordinates"])
        final_msg = msg + distance + source_location
        email_data["msg"] = final_msg
        res = self.send_email(email_data)
        if res == 1:
            print("=================Email sent to driver!================")
        elif res == 0:
            print("=========Email needs to be verified by driver! ==========")
        else:
            print("=========Check email status! Mostly Throttling error or email id not valid! =========")

    # notification to customer
    def send_email_to_customer(self,cust_data):
        res = self.send_email(cust_data)
        if res == 1:
            print("=================Email sent to customer!================")
        elif res == 0:
            print("=========Email needs to be verified by customer! ==========")
        else:
            print("=========Check email status! Mostly Throttling error or email id not valid! =========")


    def send_email(self,cust_data):
        #creaating json data
        customer_data = json.dumps(cust_data)
        # connecting to endpoint to send email
        res = requests.post(self.email_url,data=customer_data)
        email_res = json.loads(res.text)
        # print(email_res)
        return email_res


    # customer trip method 
    def customer_trip(self,booking_details):
        taxi_services = Taxi_Services()
        trip_res = taxi_services.start_trip(booking_details)



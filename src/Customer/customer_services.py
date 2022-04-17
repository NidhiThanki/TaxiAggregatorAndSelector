'''author :mayuri date:4/16/2022'''


# Imports ObjectId to convert to the correct format before querying in the db
from asyncore import read
from bson.objectid import ObjectId
from random import randint
import random,json
import datetime
import requests
from src.Util.CommonUtil import CommonUtil

# customer document contains customer_name (String), email (String), and role (String) fields
class Customer_Services():
    customer_data_list = []

    def __init__(self):
        self._latest_error = ''
        config = CommonUtil.read_properties()
        self._customer_file_path = config.get("CUSTOMER_CSV_FILE").data
        self._collection_name = config.get("CUSTOMER_COLLECTION").data
        self._max_lat = float(config.get("LAT_VALUE").data)
        self._max_long = float(config.get("LONG_VALUE").data)
        self.post_url = "https://dbco8t3hz3.execute-api.us-east-1.amazonaws.com/register-customer"
        self.get_url = "https://dbco8t3hz3.execute-api.us-east-1.amazonaws.com/read-customer"
        self.book_url = "https://pjfnpvj0ce.execute-api.us-east-1.amazonaws.com/customer-book"
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Reads customer.csv one line at a time, splits them into the data fields and inserts
    def read_data_from_csv(self):
        customer_data_list = []
        with open(self._customer_file_path, 'r') as customer_fh:
            for customer_row in customer_fh:
                customer_row = customer_row.rstrip()
                if customer_row:
                    (customer_first_name, customer_last_name,customer_email,trip_indicator) = customer_row.split(',')
                            
                customer_data = {"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"customer_email":customer_email,"trip_indicator":trip_indicator}
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

    # check for area boundary
    def check_location(self,lat,long):
        if self._max_lat <=  lat <= self._max_long  and  self._max_lat <=  long <= self._max_long:
            return 1
        return -1
        
    # register one customer
    def register_one(self,customer_first_name,customer_last_name,customer_email,lat,long):
        try:
            self._latest_error = '' 
            # read customer customer details           
            res = self.get_customer_details(customer_first_name,customer_last_name)
            cust_res = json.loads(res)
            if cust_res == -1:        
                res = self.check_location(lat,long)                
                if res == 1:            
                    customer_id = self.generate_customer_id(customer_first_name,customer_last_name)
                    _timestamp=datetime.datetime.now()
                    customer_data = {"timestamp":str(_timestamp),"customer_id":customer_id,"customer_first_name": customer_first_name,"customer_last_name": customer_last_name,"customer_email":customer_email,"location":{"type":"Point","coordinates":[long,lat]},"trip_indicator":"OFF"}        
                    self.register_connection([customer_data])
                    print("==================Successful Registration!==================")
                else:
                    print("Sorry,cab service is not available in this area!")
            else:
                print("Customer already exists!!")
        except Exception as e:
            print("RegisterOneError:",str(e))

    # registers many customer from list/csv files
    def register_many(self):
        try:
            customer_data = self.read_data_from_csv()
            for val in customer_data:
                customer_id = self.generate_customer_id(val['customer_first_name'],val['customer_last_name'])
                _timestamp=datetime.datetime.now()
                long = random.uniform(self._max_lat, self._max_long)
                lat = random.uniform(self._max_lat, self._max_long)
                val["timestamp"] = str(_timestamp)
                val["customer_id"]=customer_id
                val["location"]={"type":"Point","coordinates":[long,lat]}
                self.customer_data_list.append(val)
            self.register_connection(self.customer_data_list)
            print("==================Successful Registration!==================")
        except Exception as e:
            print("RegisterManyError:",str(e))        

    # connect to API gateway for registration
    def register_connection(self,cust_data):
        #creaating json data
        customer_data = json.dumps(cust_data)
        # connecting to endpoint to send data
        response = requests.post(self.post_url,data=customer_data)
        if response.status_code == 200:
            print("Connected to Register API Endpoint")
        else:
            print("Check status!")

    # API endpoint to read customer details
    def get_customer_details(self,customer_first_name,customer_last_name):
        try:
            cust_data = {"customer_first_name":customer_first_name,"customer_last_name":customer_last_name}
            # connecting to endpoint to send data
            response = requests.get(self.get_url,params = cust_data)            
            return response.text
        except:
            return -1

    # raise booking request and return nearest taxi
    def booking(self,customer_first_name,customer_last_name,dest_lat,dest_long):
        try:
            # read customer customer details           
            res = self.get_customer_details(customer_first_name,customer_last_name)
        except Exception as e:
            print(str(e))         
        read_res = json.loads(res)
        if read_res != -1:
            cust_loc= read_res["location"]
            cust_lat = cust_loc["coordinates"][1]
            cust_long = cust_loc["coordinates"][0]
            loc_res = self.check_location(cust_lat,cust_long)
            if loc_res != -1 :
                # connecting to endpoint to send data
                cust_id = read_res["customer_id"]
                cust_data = {"customer_id": cust_id,"cust_lat":cust_lat,"cust_long":cust_long,"type":"Point","dest_lat":dest_lat,"dest_long":dest_long}
                response = requests.get(self.book_url,params = cust_data)
                book_res = json.loads(response.text)

                if response.status_code == 200 and book_res != -1:
                    print("Connected to Booking API Endpoint")
                    print("=========Booking Successful !!===========")
                    return response.text
                else:
                    print(f"Check status:{response.text}")
                    return -1
            else:
                print("Sorry,cab service is not available in this area!")                
        else:
            return 0  

                

            
            




    

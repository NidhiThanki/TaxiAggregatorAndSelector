from src.Taxi.register_taxi_services import Register_Taxi_Services
from src.Customer.customer_services import Customer_Services
import json

# # This methods are used for get taxi data from CSV and pushing those into mongo db atlas
# print("###########################Taxi Services#################################")
# taxi_services = Register_Taxi_Services()
# taxi_services.read_data_from_csv()
# taxi_services.insert_data_db()


print("###########################Customer Services#################################")
# create customer object
cust = Customer_Services()

# # register number of customers at once
# cust.register_many()

# register one new customer
cust1 = Customer_Services()
cust1.register_one("Boba","Fetti","boba@gmail.com",12.89,77.50)

# Randomly booking for customers who are already registered for cab services
res=cust1.booking("Boba","Fetti",12.94,77.43)
if res == 0:
    print("Customer not registered for services!")
elif res !=-1:
    print("Taxi Details: ",res)
else:
    print("=========Booking Unsuccessful !!=========")


# Book for all registered customers
cust_obj = Customer_Services()
customer_details = cust_obj.get_registered_customers()
customer_details = json.loads(customer_details)

for customers in customer_details:
    customer_first_name= customers["customer_first_name"]
    customer_last_name= customers["customer_last_name"]
    lat = 12.51
    long = 77.5
    res=cust_obj.booking(customer_first_name,customer_last_name,lat,long)
    if res == 0:
        print("Customer not registered for services!")
    elif res !=-1:
        print("Taxi Details: ",res)
    else:
        print("=========Booking Unsuccessful!!=========")
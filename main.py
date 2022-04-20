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

# # registration simulation: register number of customers at once
# cust.register_many()

# register one new customer via API
cust1 = Customer_Services()
# cust1.register_one("Captain","A","captA@gmail.com","Premium")
cust1.register_one("Boba","Fett","bobaF@gmail.com","General",12.51,77.12)


# # get registered customer details
# res=cust1.get_customer_details("Boba","Fett")
# print(res)

# # get all registered customers details
# cust_obj = Customer_Services()
# customer_details = cust_obj.get_registered_customers()
# customer_details = json.loads(customer_details)
# print(customer_details)

# # Booking Simulation for all registered customers
# for customers in customer_details:
#     customer_first_name= customers["customer_first_name"]
#     customer_last_name= customers["customer_last_name"]

#     taxi_type = "ALL"
#     res=cust_obj.booking(customer_first_name = customer_first_name,customer_last_name=customer_last_name,source_lat=12.51,source_long=77.12,dest_lat=12.94,dest_long=77.43,taxi_type=taxi_type)
#     if res == 0:
#         print("Customer not registered for services!")
#     elif res !=-1:
#         print("Taxi Details: ",res)
#         print("=======================================")
#     else:
#         print("=========Booking Unsuccessful!!=========")


# # Randomly booking for customers who are already registered for cab services via API
# res=cust1.booking(customer_first_name ="Captain",customer_last_name="A",source_lat=12.51,source_long=77.12,dest_lat=12.94,dest_long=77.43,taxi_type="Basic")
res=cust1.booking(customer_first_name ="Boba",customer_last_name="Fett",source_lat=12.60,source_long=77.20,dest_lat=12.94,dest_long=77.43,taxi_type="Deluxe")
if res == 0:
    print("Customer not registered for services!")
elif res !=-1:
    print("Taxi Details: ",res)
else:
    print("=========Booking Unsuccessful !!=========")
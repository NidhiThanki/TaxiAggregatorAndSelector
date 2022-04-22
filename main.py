from src.Taxi.taxi_services import Taxi_Services
from src.Customer.customer_services import Customer_Services
import json

# print("###########################Taxi Services#################################")
# Taxi Service Object
taxi_services = Taxi_Services()

# This method will register taxies from csv file
#taxi_services.register_taxi_from_csv()

# This method will register single taxi
#taxi_services.register_single_taxi("KA05A7845", "Deluxe", "Toyota RAV4")
print("Taxi Registered !!")

print("###########################Customer Services#################################")
# create customer object
cust = Customer_Services()

# # registration simulation: register number of customers at once
# cust.register_many()

# register one new customer via API
cust1 = Customer_Services()
#cust1.register_one("James","Valdez","JamesDez@gmail.com","General",12.73,77.56)


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

res=cust1.booking(customer_first_name ="James",customer_last_name="Valdez",source_lat=12.65,source_long=77.56,dest_lat=12.94,dest_long=77.43,taxi_type="All")
if res == 0:
    print("Customer not registered for services!")
elif res !=-1:
    print("Taxi Details: ",res)
    # This method will start trip
    taxi_services.start_trip(res)
else:
    print("=========Booking Unsuccessful !!=========")



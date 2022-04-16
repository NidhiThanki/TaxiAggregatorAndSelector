from src.Taxi.register_taxi_services import Register_Taxi_Services
from src.Customer.customer_services import Customer_Services

# This methods are used for get taxi data from CSV and pushing those into mongo db atlas
print("###########################Taxi Services#################################")
taxi_services = Register_Taxi_Services()
taxi_services.read_data_from_csv()
taxi_services.insert_data_db()


print("###########################Customer Services#################################")
# create customer object
cust1 = Customer_Services()
# register number of customers at once
cust1.register_many()

# # register one new customer
# cust1.register_one("Mohan","Kumar","moh@gmail.com",13.950290,77.204570)

# # Randomly booking for customers who are already registered for cab services
# res=cust1.booking("Mohan","Kumar")
# if res !=-1:
#     print("=========Booking Successful !!===========")
#     print("Taxi Details: ",res)
# else:
#     print("=========Booking Unsuccessful !!=========")


from src.Taxi.taxi_services import Taxi_Services
from src.Customer.customer_services import Customer_Services
from multiprocessing.pool import ThreadPool as Pool
import json
import random


def main():    
    print("########################### Simulation: Book A Trip Service #################################")
    # Customer Service Object
    cust_obj = Customer_Services()    
    '''get all registered customers details'''    
    customer_details = []
    customer_details = cust_obj.get_registered_customers()
    customer_details = json.loads(customer_details)
    ''' Async Booking Simulation for all registered customers'''
    if len(customer_details) > 0:
        pool_size=len(customer_details)
        if pool_size > 10:
            pool_size=50
        pool = Pool(pool_size) 
        for customers in customer_details:
            customer_first_name= customers["customer_first_name"]
            customer_last_name= customers["customer_last_name"]
            # random taxi type selection
            taxi_type_list = ["Basic","Deluxe","Luxury","ALL"]
            random.shuffle(taxi_type_list)
            taxi_type = taxi_type_list[0]
            # random lat long generation from area boundary 
            source_lat = random.uniform(12.5000001,12.972442 )
            source_long = random.uniform(77.1000001, 77.580643)
            dest_lat = random.uniform(12.5000001,12.972442 )
            dest_long = random.uniform(77.1000001, 77.580643)
            result = pool.apply_async(cust_obj.booking, (customer_first_name,customer_last_name,source_lat,source_long,dest_lat,dest_long,taxi_type))
        pool.close()
        pool.join() 
      
    
    # print("###########################Taxi Services#################################")
    # # Taxi Service Object
    # taxi_services = Taxi_Services()
    # # This method will register single taxi
    # taxi_services.register_single_taxi("KA05A2849", "Deluxe", "Toyota RAV4")
    # print("Taxi Registered !!")

    # # This method will register taxies from csv file
    # taxi_services.register_taxi_from_csv()


    # # print("###########################Customer Services#################################")
    # '''register a new customer via API'''
    # cust1 = Customer_Services()
    # cust1.register_one("Rohit","K","rohitK@gmail.com","Premium",12.73,77.56)
    

    # # get registered customer details
    # res=cust1.get_customer_details("Rohit","K")
    # print(res)

    # '''Randomly booking for customers who are already registered for cab services via API'''
    # book_res=cust1.booking(customer_first_name ="Rohit",customer_last_name="K",source_lat=12.60,source_long=77.20,dest_lat=12.94,dest_long=77.43,taxi_type="Deluxe")
   
    # if book_res == 0:
    #     print("Customer not registered for services!")
    # elif book_res !=-1:
    #     print("Taxi Details: ",book_res)    
    # else:
    #     print("=========Booking Unsuccessful !!=========")

    # # '''This method will start trip'''
    # if book_res == 1:
    #     taxi_services.start_trip(book_res)





if __name__ == "__main__":
    main()
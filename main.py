from src.Taxi.taxi_services import Taxi_Services
from src.Customer.customer_services import Customer_Services
from multiprocessing.pool import ThreadPool as Pool
import json
import random,string


def main():    
    print("########################### Taxi Registration Simulation####################################")
    taxi_services = Taxi_Services()
    taxi_type_list_for_registration = ["Basic", "Deluxe", "Luxury"]
    taxi_names = [{"Basic": ["Maruti Alto 800", "Maruti Wagon R"]},
                  {"Deluxe": ["Toyota Rav4", "Toyota Venza"]}, {"Luxury": ["Tesla", "Audi A4"]}]
    pool_size =50
    pool = Pool(pool_size) 
    try: 
        for taxi in range(0,50):
            # random data generation for taxi registration
            taxi_type = random.choice(taxi_type_list_for_registration)
            selected_idx = taxi_type_list_for_registration.index(taxi_type)
            taxi_name_list = taxi_names[selected_idx].get(taxi_type)
            registration_plate_no = "KA0" + str(random.randint(5, 8)) + random.choice(string.ascii_uppercase) \
                                    + str(random.randint(1000, 9999))
            # register taxi
            result = pool.apply_async(taxi_services.register_single_taxi,(registration_plate_no, taxi_type, random.choice(taxi_name_list)))
        pool.close()
        pool.join()    
    except Exception as e :
        print("Taxi Registration Error: ",str(e)) 

    print("########################### Customer Registration Simulation #################################")
    cust_reg_service = Customer_Services()
    # random data generation for customer registration
    email_id_list = ["aarondouyere25@gmail.com", "mayuri.phanslkr@gmail.com", "nidhi.thanky@gmail.com",
                    "pavantalur@gmail.com"]
    customer_type_list = ["Premium", "Non-Premium"]  
    pool_size = 5  
    pool = Pool(pool_size)
    try:
        for customer in range(0,5):
            first_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
            last_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
            email = random.choice(email_id_list)
            customer_type = random.choice(customer_type_list)
            lat = random.uniform(12.5000001, 12.972442)
            long = random.uniform(77.1000001, 77.580643)
            # mobile number generation
            range_start = 10**(10-1)*random.randint(6, 9)
            range_end = (10**10)-1
            mobile_number=random.randint(range_start, range_end)
            # register customer
            result = pool.apply_async(cust_reg_service.register_one, (first_name, last_name, email, customer_type, lat, long, mobile_number))
        pool.close()
        pool.join()    
    except Exception as e :
        print("Customer Registration Error: ",str(e)) 

    print("########################### Update Customer Data ###################################")
    cust_updt_service = Customer_Services()

    current_mobile_number = mobile_number
    new_customer_email = random.choice(email_id_list)
    new_customer_type = random.choice(customer_type_list)    
    # new mobile number generation
    range_start = 10**(10-1)*random.randint(6, 9)
    range_end = (10**10)-1
    new_mobile_number=random.randint(range_start, range_end)    

    cust_updt_service.updt_customer_data(new_customer_email=new_customer_email,new_customer_type=new_customer_type,current_mobile_number=current_mobile_number
    ,new_mobile_number=new_mobile_number)

    print("########################### Read Customer Data ################################################")
    cust_read_service = Customer_Services()
    read_res = cust_read_service.get_customer_details(new_mobile_number)
    print(read_res)


    print("########################### Book Trip for Customers Asynchronously ###################")
    try:
        # Customer Service Object
        cust_book_service = Customer_Services()
        '''get all registered customers details'''    
        customer_details = []
        premium_cust_mobile_list = []
        customer_details = cust_book_service.get_registered_customers()
        customer_details = json.loads(customer_details)
        # creating list of premium customers for simulating "other" book_type scenario 
        for val in customer_details:
            if val["customer_type"].lower() == "premium":
                premium_cust_mobile_list.append(val["mobile_number"])
        ''' Async Booking Simulation for all registered customers'''
        if len(customer_details) > 0:
            pool_size=len(customer_details)
            if pool_size > 10:
                pool_size=50
            pool = Pool(pool_size)
            taxi_type_list = ["Basic","Deluxe","Luxury","ALL"]            
            for customers in customer_details:
                try:
                    # random taxi type selection                    
                    random.shuffle(taxi_type_list)
                    taxi_type = taxi_type_list[0]
                    book_type_list = ["self","other"]
                    book_type = random.choice(book_type_list)
                    '''booking for non-registered customers i.e. "other customers" using premium customer aggregator's mobile number'''
                    if book_type == "other":
                        mobile_number = random.choice(premium_cust_mobile_list)
                        customer_first_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
                        customer_last_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
                    else:
                        ''' booking for registered customers i.e. non-premium and premium custoemrs for bokking type as self '''
                        mobile_number = customers["mobile_number"]
                        customer_first_name= customers["customer_first_name"]
                        customer_last_name= customers["customer_last_name"]
                    # random lat long generation from area boundary 
                    source_lat = random.uniform(12.5000001,12.972442 )
                    source_long = random.uniform(77.1000001, 77.580643)
                    dest_lat = random.uniform(12.5000001,12.972442 )
                    dest_long = random.uniform(77.1000001, 77.580643)
                    result = pool.apply_async(cust_book_service.booking, (customer_first_name,customer_last_name,source_lat,source_long,dest_lat,dest_long,taxi_type,mobile_number,book_type))
                except Exception as e:
                    print("Internal booking for loop error: ",str(e))
            pool.close()
            pool.join() 
    except Exception as e:
        print("Booking for loop Error: ",str(e))

   
   

if __name__ == "__main__":
    main()
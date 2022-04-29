import string
import random

from src.Taxi.taxi_services import Taxi_Services
from src.Customer.customer_services import Customer_Services

taxi_type_list_for_registration = ["Basic", "Deluxe", "Luxury"]
taxi_names = [{"Basic": ["Maruti Alto 800", "Maruti Wagon R"]},
              {"Deluxe": ["Toyota Rav4", "Toyota Venza"]}, {"Luxury": ["Tesla", "Audi A4"]}]
registration_plate_no = "KA0" + str(random.randint(5, 8)) + random.choice(string.ascii_uppercase) \
                        + str(random.randint(1000, 9999))

# random data generation for taxi registration
taxi_type = random.choice(taxi_type_list_for_registration)
selected_idx = taxi_type_list_for_registration.index(taxi_type)
taxi_name_list = taxi_names[selected_idx].get(taxi_type)

# register taxi
taxi_services = Taxi_Services()
taxi_services.register_single_taxi(registration_plate_no, taxi_type, random.choice(taxi_name_list))



email_id_list = ["aarondouyere25@gmail.com", "mayuri.phnslkr@gmail.com", "nidhi.thanky@gmail.com",
                 "pavantalur@gmail.com"]
customer_type_list = ["Premium", "General"]

# random data generation for customer registration

first_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
last_name = random.choice(string.ascii_uppercase) + "".join(random.choice(string.ascii_lowercase) for i in range(5))
email = random.choice(email_id_list)
customer_type = random.choice(customer_type_list)
lat = random.uniform(12.5000001, 12.972442)
long = random.uniform(77.1000001, 77.580643)

# register customer
customer_service = Customer_Services()
customer_service.register_one(first_name, last_name, email, customer_type, lat, long)

# random data generation for taxi booking
taxi_type_list_for_booking = ["Basic", "Deluxe", "Luxury", "ALL"]
source_lat = random.uniform(12.5000001, 12.972442)
source_long = random.uniform(77.1000001, 77.580643)
dest_lat = random.uniform(12.5000001, 12.972442)
dest_long = random.uniform(77.1000001, 77.580643)

# book taxi
customer_service.booking(first_name, last_name, source_lat, source_long, dest_lat, dest_long,
                         random.choice(taxi_type_list_for_booking))

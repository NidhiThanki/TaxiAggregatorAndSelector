from src.Taxi.register_taxi_services import Register_Taxi_Services

# This methods are used for get taxi data from CSV and pushing those into mongo db atlas
taxi_services = Register_Taxi_Services()
taxi_services.read_data_from_csv()
taxi_services.insert_data_db()
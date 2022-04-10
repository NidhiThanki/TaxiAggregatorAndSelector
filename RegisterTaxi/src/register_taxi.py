from src.Services.register_taxi_services import Register_Taxi_Services

taxi_services = Register_Taxi_Services()
taxi_services.read_data_from_csv()
taxi_services.insert_data_db()


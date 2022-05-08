''' author: mayuri date: 04/24/2022'''

# TaxiAggregatorAndSelector

main.py
- is a driver file.
- have code to create customer and taxi objects.
- can be used to read registered customer or taxis.
- can be used to update registered customer data.
- used for creating taxi booking for registered customers asynchronously.

src folder
- Config folder : contains configuration files.
	- customer csv file
	- taxi csv file
	- area boundary json structure
	- app-config properties file which contains API Gateway URLs
- Custoemr folder : contains customer script
	- Customer_Service class: used for creating customer object and access customer data using different methods defined.
	- Methods:
		- _location_data_json : sets service area boundary for start and end latitude and longitudes.
		- read_data_from_csv : reads customer data from csv.
		- generate_customer_id : creates unique customer id while registration of each customer.
		- check_location : checks if customer's location is within servie area boundary 
						- if customer not within boundry area then drops request immediately.
		- register_one : 
			- get required data for customer registration.
			- offers customer duplication check based on mobile number(unique)
		- register_many : creates required customer data list from csv
		- register_connection : connects to registration API endpoint.
		- updt_customer_data : 
			- update customer details.
			- offers modification in customer email,type and mobile number.
		- get_customer_details : returns all registered customer details.
		- get_registered_customers : returns customer details based on customer's mobile number
		- booking : 
			- makes booking based on user types : General(not registered), Premium(registered), Non-premium(registered)
			- if user type is General: 
				- booking not allowed if such customer is already in trip i.e. if customer's trip indicator is ON.
				- booking not allowed for third-party or outside customers.
			-if user type is Premiun: 
				- booking allowed if such customer is already in trip i.e. if customer's trip indicator is ON.
				- booking allowed for third-party or outside customers with premium number mobile number check.
		- send_email : sends email to customer with comments and suggestions.
		- customer_trip : invokes trip method for taxi.
- Taxi folder : contains taxi script
	- used for creating taxi object from taxi class
	- used to access taxi data using different methods defined.
	- It has taxi_registration, get_taxi details and start_trip methods.
	- Above mentioned methods access API gateway which triggers Lambda functions and ingest data in database
- Util folder : contains code to read and handle config files.


LambdaFunctions : contains lambda function scripts
	- customer-book-lambda : script used for handling request received at customer-book endpoint.
		- connects with mongodb atlas.
		- creates booking based on customer request.
		- provides taxi for customer:
			- check if taxi is available within 10km with customer's taxi type preference.
			- if customer request is not fullfilled then booking fails.
			- if booking fails due to taxitype prefernce or 10 km range limit then provides customer with best option/suggestion for nearest taxi.
			- if booking is successful:
				- sets trip indicator from "OFF" for taxi and customer to "ON" in their respective mongodb collection.
				- for outside/unregistered customer booking is created using premium member custoemr id and email while customer type is set to "other" in booking collections.
	- read-customer : script used for handling request received at read-customer endpoint.
		- connects with mongodb atlas.
		- returns customer data based on request type "all" or "one"
			- if request type is all : returns data for all registered customers.
			- if request type is one : returns data for required registered customer.
	- register-customer : script used for handling request received at register-customer endpoint.
		- connects with mongodb atlas.
		- register customer data based on request type "all" or "one"
			- if request type is all : registers list of customers.
			- if request type is one : registers one customer.
	- update_customer_data : script used for handling request received at update-customer endpoint.
		- connects with mongodb atlas.
		- update customer details like mobile number,email,customer type.
	- get_location_updates:
	    - Gets the taxi's location data
	    - It returns list of location data of taxi within given time range
	- get_taxi_details:
	    - Returns details of taxi
	    - Used to verify taxi details while insertion
	- register_taxi:
	    - Registers taxi's details into database
	-send_email:
	    - It sends email notification to customer and drivers
	Taxi_Trip:
	    - It simulates taxi from source location to destination location.
	    - Based on total distance it calculates geo_points using numpy, geopy libraries
	    - It ingest calculated geo points into database with timestamp
	    - Instead of using sleep() method to put data into database with some delay, it calculates future timestamp and ingest data into database
	    - Taxi is moving at speed of 1 km per 1 min in simulation code
	    - Once taxi is reached to destination it ends the trip the updates trip_indicator for customer and taxi and also updates current location of taxi

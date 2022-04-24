''' author: mayuri dte: 04/24/2022'''

# TaxiAggregatorAndSelector

main.py
- is a driver file.
- have code to create customer and taxi objects.
- can be used to read default customer or taxis from csv file.
- used for creating taxi booking for registered customers asynchronously.

src folder
- Config folder : contains configuration files.
		- customer csv file
		- taxi csv file
		- area boundary json structure
- Custoemr folder : contains customer script
			- used for creating customer object from custoemr service class.
			- used to access customer data using different methods defined.
- Taxi folder : contains taxi script
			- used for creating taxi object from taxiclass
			- used to access taxi data using different methods defined.
- Util folder : contains code to read and hadle config files.
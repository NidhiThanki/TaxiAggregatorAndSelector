'''author :mayuri date:4/16/2022'''


from pymongo import MongoClient
import pprint
import json

def lambda_handler(event,context):
    try:
        cust_data=event['queryStringParameters']        
        print(cust_data)        
        #Access the MongoDB Service
        db_uri="mongodb+srv://capstone:capstone@capstone.ufkam.mongodb.net/taxi_aggregation_selection?retryWrites=true&w=majority"
        aggregator_cli = MongoClient(db_uri)
        # Database
        aggregator_db = aggregator_cli['taxi_aggregation_selection']
        # Collection
        customers = aggregator_db['customer_registration_data']   
        if cust_data["req"] == "all":
            # registered customers list
            reg_cust_list=[]
            for doc in customers.find():
                doc.pop('_id')
                reg_cust_list.append(doc)
            if len(reg_cust_list) > 0:
                return reg_cust_list
            return -1
        else:
            customer_data = -1
            cust_first_name = cust_data["customer_first_name"]
            cust_last_name = cust_data["customer_last_name"]
            try:
                for doc in customers.find():
                    doc.pop('_id')
                    if doc["customer_first_name"] == cust_first_name and doc["customer_last_name"] == cust_last_name :
                        customer_data= doc
                return customer_data                
            except Exception as e:
                pprint.pprint(str(e))
                return -1
    except Exception as e:
        pprint.pprint(str(e))
        return -1

        

from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from random import randint

# customer document contains customer_name (String), email (String), and role (String) fields
class customer():
    CUSTOMER_COLLECTION = 'customers'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        # self.customer_data=customer_data
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    #  this provides a way to fetch the customer document based on the customer_name
    def find_by_customer_name(self, customer_name):
        key = {'customer_name': customer_name}       
        return self.__find(key)

    # Since customer_name should be unique in customers collection, this provides a way to fetch the customer document based on the customer_name
    def find_by_customer_id(self, customer_id):
        key = {'customer_id': customer_id}       
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        try:
            try:
                customer_document = dict(self._db.get_single_data(customer.CUSTOMER_COLLECTION,{'customer_name':key['customer_name']}))
                return customer_document
            except:
                try:
                    customer_document = dict(self._db.get_single_data(customer.CUSTOMER_COLLECTION,{'customer_id':key['customer_id']}))
                    return customer_document
                except:
                    try:
                        customer_document = dict(self._db.get_single_data(customer.CUSTOMER_COLLECTION,{'_id':key['_id']}))
                        return customer_document
                    except:
                        return -1                    
        except Exception as e:
            print("E:",str(e))
            return -1  
 
        
    def generate_customer_id(self,cust_name):
        start = randint(1,10)
        end = randint(11,20)
        rand_num = randint(start,end)
        cust_name = cust_name.replace(" ","")
        cust_id = f"{cust_name}_{rand_num}"
        # check if customer id already exists
        res = self.find_by_customer_id(cust_id)
        if res == -1:
            return cust_id
        # extra step for uniq user id generate
        else:
            rand_num = randint(220,320)
            cust_id = f"{cust_name}_{rand_num}"
            return cust_id
        
    # This first checks if a customer already exists with that customer_name. If it does, it populates latest_error and returns -1
    # If a customer doesn't already exist, it'll insert a new document and return the same to the caller
    def register(self,customer_name,customer_longitude,customer_latitude):
        try:
            self._latest_error = ''               
            cust_name_document = self.find_by_customer_name(customer_name)
            if (cust_name_document) != -1 :          
                self._latest_error = f'Customer: {customer_name} already exists !'
                return -1           
            else:
                customer_id = self.generate_customer_id(customer_name)
                customer_data = {'customer_id':customer_id,'customer_name': customer_name,'customer_location':f"[{customer_longitude},{customer_latitude}]"}
                customer_obj_id = self._db.insert_single_data(customer.CUSTOMER_COLLECTION, customer_data)
                return self.find_by_object_id(customer_obj_id)        
        except Exception as e:
            print("Error:",str(e))
            return -1

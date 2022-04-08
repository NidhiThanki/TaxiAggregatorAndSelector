
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


# customer document contains customer_name (String), email (String), and role (String) fields
class customer():
    CUSTOMER_COLLECTION = 'customers'

    def __init__(self,logged_customer_id):
        self._db = Database()
        self._latest_error = ''
        self.logged_customer_id=logged_customer_id
    
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
                customer_document = dict(self._db.get_single_data(customer.CUSTOMER_COLLECTION,{'customer_id':self.logged_customer_id}))      
                customer_id=customer_document['customer_id']           
                customer_data= dict(self._db.get_single_data(customer.CUSTOMER_COLLECTION,key))
                return customer_data
            except:
                self._latest_error = f'{self.logged_customer_id} not found!'  
                return -1  
        except Exception as e:
            customer_id=key['customer_id']
            self._latest_error = f'{customer_id} not found!'  
            return -1 
        
    
    # This first checks if a customer already exists with that customer_name. If it does, it populates latest_error and returns -1
    # If a customer doesn't already exist, it'll insert a new document and return the same to the caller
    def register(self,  customer_id, customer_name,customer_longitude,customer_latitude):
        try:
            self._latest_error = ''               
            cust_id_document = self.find_by_customer_id(customer_id)
            if self.logged_customer_id != customer_id:
                self._latest_error = f'Customer ID Error!'
                return -1

            if (cust_id_document) != -1 :                
                self._latest_error = f'Customer ID: {customer_id} already exists for another Customer: {cust_id_document["customer_name"]}!'
                return -1
            else:
                customer_data = {'customer_id':customer_id,'customer_name': customer_name,'customer_location':f"[{customer_longitude},{customer_latitude}]"}
                customer_obj_id = self._db.insert_single_data(customer.CUSTOMER_COLLECTION, customer_data)
                return self.find_by_object_id(customer_obj_id)        
        except Exception as e:
            print(str(e))
            return -1

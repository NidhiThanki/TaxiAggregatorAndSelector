from customer import customer

# create customer object with uid
cust_1=customer()
# register customer
register_user_data=cust_1.register("Tim Frank","12.950290","77.604570")
if (register_user_data == -1):
    print(cust_1.latest_error)
else:
    print(f"Inserted Data: {register_user_data}")

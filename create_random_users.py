from pymongo import MongoClient
import names
import random
import string
# Make a connection to Mongo server
client = MongoClient('localhost', 27017)

# initialize db instance 
db = client["training-delta"]

# see all collections present in this db
users = db['users']

for i in range(5):
    source = string.ascii_letters + string.digits
    u_id = ''.join((random.choice(source) for d in range(32)))
    u_id = u_id.upper()
    source_time = string.digits
    unix_time = '16' + ''.join((random.choice(source_time) for t in range(8)))
    user_name = names.get_full_name()
    response = users.insert_one({
      "guid": u_id,
      "expire":  unix_time,
      "user": user_name
    })
    print(response.inserted_id)

# client["training-delta"]['users'].insert_one({"name": "david", "phone": 1245373748})


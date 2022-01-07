from flask import Flask
from flask_restful import Resource, Api, reqparse
import random
import string
import time
import re
from pymongo import MongoClient
import json
from datetime import datetime

# Make a connection to Mongo server
client = MongoClient('localhost', 27017)

# initialize db instance
db = client["training-delta"]

# see all collections present in this db
users = db['users']


def verify_guid(guid):
    yes_count = len(re.findall("[A-Z0-9]", guid))
    all_count = len(guid)
    if yes_count == all_count and all_count == 32:
        return True
    return False


def check_or_generate_time(expire=None):
    if not expire:
        # adds 30 days to current date
        unix_time = int(time.time()) + 2592000
        return unix_time
    else:
        return expire


def update_server_log(data, method):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open("server.log", "a")
    prepare_to_log = json.dumps(data)
    f.write("[" + current_time + "] " + method + ' reponse: ' + prepare_to_log + "\n")
    f.close()


# get random string of letters and digits
source = string.ascii_letters + string.digits
result_guid = ''.join((random.choice(source) for i in range(20)))

# Initialize App object from Flask
app = Flask(__name__)
api = Api(app)


# Create Resource

# endpoint with slash and guid
class GuidWithSlash(Resource):
    def get(self, u_id):
        if verify_guid(u_id):
            search_user = users.find_one({'guid': u_id})
            if search_user:
                data = {
                    "guid": u_id,
                    "expire": search_user['expire'],
                    "user": search_user['user']
                }
                update_server_log(data, 'GET')
                return data
            else:
                data = {"msg": "no users were found"}
                update_server_log(data, 'GET')
                return data
        else:
            data = {"msg": "Guid is not valid"}
            update_server_log(data, 'GET')
            return {"msg": "Guid is not valid"}

    def post(self, u_id):
        parser = reqparse.RequestParser()
        parser.add_argument('expire', location='json')
        parser.add_argument('user', location='json')
        args = parser.parse_args()
        user = args['user']
        expire = check_or_generate_time(args["expire"])
        if verify_guid(u_id):
            users.insert_one({"guid": u_id, "expire": expire, "user": user})
            data = {
                "guid": u_id,
                "expire": expire,
                "user": user
            }
            update_server_log(data, 'POST')
            return data
        else:
            data = {"msg": "Guid is not valid"}
            update_server_log(data, 'POST')
            return data

    def patch(self, u_id):
        parser = reqparse.RequestParser()
        parser.add_argument('expire', location='json')
        parser.add_argument('user', location='json')
        args = parser.parse_args()
        user = args['user']
        expire = check_or_generate_time(args["expire"])
        if verify_guid(u_id):
            search_user = users.find_one({'guid': u_id})
            if search_user:
                new_user_values = {"$set": {"guid": u_id, "expire": expire, "user": user}}
                users.update_one(search_user, new_user_values)
                data = {
                    "guid": u_id,
                    "expire": expire,
                    "user": user
                }
                update_server_log(data, 'PATCH')
                return data
            else:
                data = {"msg": "No user was found"}
                update_server_log(data, 'PATCH')
                return data
        else:
            data = {"msg": "Guid is not valid"}
            update_server_log(data, 'PATCH')
            return data

    def delete(self, u_id):
        if verify_guid(u_id):
            users.delete_one({"guid": u_id})
            data = {"msg": "User was removed"}
            update_server_log(data, 'DELETE')
            return data
        else:
            data = {"msg": "Guid is not valid"}
            update_server_log(data, 'DELETE')
            return data


# endpoint without guid
class Random_guid(Resource):
    def post(self):
        u_id = ''.join((random.choice(source) for i in range(32)))
        u_id = u_id.upper()
        parser = reqparse.RequestParser()
        parser.add_argument('expire', location='json')
        parser.add_argument('user', location='json')
        args = parser.parse_args()
        user = args['user']
        expire = check_or_generate_time(args['expire'])
        users.insert_one({
            "guid": u_id,
            "expire": expire,
            "user": user
        })
        data = {
            "guid": u_id,
            "expire": expire,
            "user": user
        }
        update_server_log(data, 'POST')
        return data


# Create endpoint
api.add_resource(Random_guid, '/guid')
api.add_resource(GuidWithSlash, '/guid/<u_id>')

if __name__ == '__main__':
    # Run Flask-server
    app.run()

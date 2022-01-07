This is a flask mongo project
written by Vraja Das

address of api : http://127.0.0.1:5000/guid
Instruction to use the Api:

GET: (add GUID to the address: http://127.0.0.1:5000/guid/QBXZVMQHETYJM08BV2Z16FSZDQFU2PFB)
Request parameters 
in address : GUID: must be 32 characters, numbers and letters only uppercase
response: in json format, expire unix date and full name

POST: 
(add GUID to the address: http://127.0.0.1:5000/guid/QBXZVMQHETYJM08BV2Z16FSZDQFU2PFB)
Request parameters 
in address : GUID: must be 32 characters, numbers and letters only uppercase
in body, json format:
'expire': unix date, number format 
(if date = null, api will create a date which is current date + 30 days.)
'user': the user's full name
Creates a new user with the guid that was sent. returns user details of user in json format (guid,expire,user).

PATCH: (add GUID to the address: http://127.0.0.1:5000/guid/QBXZVMQHETYJM08BV2Z16FSZDQFU2PFB)
in body, json format:
'expire': unix date, number format 
(if date = null, api will create a date which is current date + 30 days.)
'user': the user's full name
updates a user nd returns new details

DELETE :
(add GUID to the address: http://127.0.0.1:5000/guid/QBXZVMQHETYJM08BV2Z16FSZDQFU2PFB)
Removes the user from database and returns a msg: 'User was removed'


POST: To create a user without the guid send Post request to: http://127.0.0.1:5000/guid
in body, json format:
'expire': unix date, number format 
(if date = null, api will create a date which is current date + 30 days.)
'user': the user's full name 
This api will generate a random guid and return new user detail:(guid,expire,user)

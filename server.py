from flask import Flask, request, json
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
# from json import dumps
from flask_jsonpify import jsonify

# 1 - As a user, I need an API to create a friend connection between two email addresses.
#	{"friends":["andy@example.com","john@example.com"]} == {"success": true}
# 2 - As a user, I need an API to retrieve the friends list for an email address.
#	{"email": "andy@example.com"} == { "success": true, "friends" : ['john@example.com'],"count" : 1}
# 3 - As a user, I need an API to retrieve the common friends list between two email addresses.
#	{"friends":['andy@example.com','john@example.com'] == {"success": true, "friends" :['common@example.com'],"count" : 1}
# 4 - As a user, I need an API to subscribe to updates from an email address.
# 	{"requestor": "lisa@example.com",  "target": "john@example.com"} == {"success": true}
# 5 - As a user, I need an API to block updates from an email address.
#	{"requestor": "andy@example.com", "target": "john@example.com"} == {"success": true}
# 6 - As a user, I need an API to retrieve all email addresses that can receive updates from an email address.
#	{"sender":  "john@example.com","text": "Hello World! kate@example.com"} == {"success": true, "recipients":["lisa@example.com","kate@example.com"]}

app = Flask(__name__)

# List of users
# Example ['andy@example.com','john@example.com']
uList = []

# List of friends connection
# Example [['andy@example.com','john@example.com'],
#			['andy@example.com','common@example.com'],
#			['john@example.com','common@example.com']]
uFriendList = []

# List of subscriber 
# Example [{'lisa@example.com':'john@example.com'}]
uSubscribeList = []

# List of blocked 
# Example [{'andy@example.com','john@example.com'}]
uBlockList = []

### 1 - As a user, I need an API to create a friend connection between two email addresses.
### 	Dependencies	- Story #5 (Done) / try..catch (To Do)	
###		Validation		- N.A
###		Assumption		
###			- Create friends connection between 2 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0101 / Server error, please contact administrator
###			0102 / Bad request, please correct and sumbit request again
###			0103 / Friend on block list
###			0104 / Friend connection exist
@app.route('/create', methods = ['POST'])
def create_friend_conn():
	tempList=[]
	result = {}
	error = []
	
	### Retrieve the request JSON body
	json_data = request.data
	req_data = json.loads(request.data)
	print(json_data)
	print(req_data)
	
	### Parse the "friend" list and append to user list
	for user in req_data['friends']:
		if user not in uList:
			uList.append(user)
		tempList.append(user)
	
	print(tempList)
	
	### Make the request data order consistent through sorting, 
	### validate against the friend list and block list 
	### before inserting into friend list
	tempList.sort()
	if tempList not in uFriendList:
		if tempList not in uBlockList:
			uFriendList.append(tempList)
		else:
			error.append("0103")
			error.append("Friend on block list")
	else:
		error.append("01014")
		error.append("Friend connection exist")
		
	### Check if error occurred
	if len(error) > 0:
		result["fail"] = "true"
		result["error"] = error
	else:
		result["success"] = "true" 

	print(uList) 
	print(uBlockList)
	print(uFriendList)
	
	return jsonify(result)

### 2 - As a user, I need an API to retrieve the friends list for an email address.
### 	Dependencies	- Story #1(Done) / try..catch (To Do)	
###		Validation		- N.A
###		Assumption		
###			- Check friends list for 1 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0201 / Server error, please contact administrator
###			0202 / Bad request, please correct and sumbit request again
###			0203 / No friends
###			0204 / User not found
@app.route('/retrieve', methods = ['POST'])
def retrieve_friends():
	tempList=[]
	result = {}
	error = []
	
	### Retrieve the request JSON body
	jason_data = request.data
	req_data = request.get_json()
	print(jason_data)
	print(req_data)
	
	email = req_data['email']
	print(email)
	
	### Parse through the uFriendList using the email from request.
	for friend in uFriendList:
		if email in friend:
			for element in friend:
				if element != email:
					tempList.append(element)
	
	print (tempList)
	
	if len(tempList) > 0:
		result["success"] = "true"
		result["friends"] = tempList
		result["count"] = len(tempList)
	else:
		result["fail"] = "true"
		error.append("0203")
		error.append("No friends")
		result["error"] = error
	
	return jsonify(result)

### 3 - As a user, I need an API to retrieve the common friends list between two email addresses.
###		Dependencies 	- try..catch (To Do)	
###		Validation		- N.A
###		Assumption		
###			- Check friends list for 2 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0301 / Server error, please contact administrator
###			0302 / Bad request, please correct and sumbit request again
###			0303 / No common friends
###			0304 / User not found
@app.route('/common', methods = ['POST'])
def retrieve_common_friend():
	tempList1=[]
	tempList2=[]
	commonList=[]
	count=0
	result = {}
	error = []
	
	### Retrieve the request JSON body
	json_data = request.data
	req_data = request.get_json()
	print(json_data)
	print(req_data)
	
	user = req_data['friends']
	print(user[0])
	print(user[1])
	
	### Create a list of friends from 2 user, as stated in user story. 
	for friend in uFriendList:
		if user[0] in friend:
			if friend[0] != user[0]:
				tempList1.append(friend[0])
			else:
				tempList1.append(friend[1])
		if user[1] in friend:
			if friend[0] != user[1]:
				tempList2.append(friend[0])
			else:
				tempList2.append(friend[1])
	
	### Compare and extract out the common friends
	for element in tempList1:
		if element in tempList2:
			commonList.append(element)
	
	print (tempList1)
	print (tempList2)
	print (commonList)
	
	if len(commonList) > 0:
		result["success"] = "true"
		result["friends"] = commonList
		result["count"] = len(commonList)
	else:
		result["fail"] = "true"
		error.append("0303")
		error.append("No common friends")
		result["error"] = error
	
	return jsonify(result)

### 4 - As a user, I need an API to subscribe to updates from an email address.
###		Dependencies 	- try..catch (To Do)	
###		Validation		- N.A
###		Assumption		
###			- Subscription for 2 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0401 / Server error, please contact administrator
###			0402 / Bad request, please correct and sumbit request again
###			0403 / Subscription exist
###			0404 / User not found
@app.route('/subscribe', methods = ['POST'])
def subscribe_to_friend():
	uSubscriber={}
	result = {}
	error = []

	### Retrieve the request JSON body
	jason_data = request.data
	req_data = request.get_json()
	print(jason_data)
	print(req_data)
	
	requestor = req_data['requestor']
	target = req_data['target']
	print(requestor)
	print(target)
	
	### Add to subscriber list
	uSubscriber[requestor]=target
	if uSubscriber not in uSubscribeList:
		uSubscribeList.append(uSubscriber)
	else:
		error.append("0403")
		error.append("Subscription exist")
	
	print(uSubscribeList)
		
	### Check if error occurred
	if len(error) > 0:
		result["fail"] = "true"
		result["error"] = error
	else:
		result["success"] = "true" 
	
	return jsonify(result)

### 5 - As a user, I need an API to block updates from an email address.
###		Dependencies 	- try..catch (To Do)	
###		Validation		- N.A
###		Assumption		
###			- Block between 2 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0501 / Server error, please contact administrator
###			0502 / Bad request, please correct and sumbit request again
###			0503 / Block exist
###			0504 / User not found
@app.route('/block', methods = ['POST'])
def block_friend():
	uBlock={}
	result = {}
	error = []
	
	### Retrieve the request JSON body
	jason_data = request.data
	req_data = request.get_json()
	print(jason_data)
	print(req_data)
	
	requestor = req_data['requestor']
	target = req_data['target']
	print(requestor)
	print(target)
	
	### Add to the block list
	uBlock[requestor]=target
	if uBlock not in uBlockList:
		uBlockList.append(uBlock)
	else:
		error.append("0503")
		error.append("Block exist")
	
	print(uBlockList)
		
	if len(error) > 0:
		result["fail"] = "true"
		result["error"] = error
	else:
		result["success"] = "true" 
		
	return jsonify(result)
	
### 6 - As a user, I need an API to retrieve all email addresses that can receive updates from an email address.
### 	Dependencies - Story #1(Done), Story #4(Done), Story #5(To Do) / try..catch(To Do)
###		Validation		- N.A
###		Assumption		
###			- Block between 2 user at 1 time only
###			- Case sensitive for input
###		Propose JSON responses for errors
###		{ 'failed' : true
###			'error' : [ "<error_code>","<error_message>" ] 
###		}
###			0601 / Server error, please contact administrator
###			0602 / Bad request, please correct and sumbit request again
###			0604 / User not found
@app.route('/retrieveSubscriber', methods = ['POST'])
def retrieve_subscriber():
	tempList=[]

	### Retrieve the request JSON body
	jason_data = request.data
	req_data = request.get_json()
	print(jason_data)
	print(req_data)
	
	sender = req_data['sender']
	text = req_data['text']
	print(sender)
	print(text)

	### Check for subscriber to the sender
	for user in uList:
		for subscriber in uSubscribeList:
			if subscriber.get(user) == sender:
				tempList.append(user)
	
	### Check for email in the text
	words = text.split()
	for word in words:
		if word.find('@')!=-1:
			tempList.append(word)
				
	print(tempList)
	
	result = {}
	result["success"] = "true"
	result["recipients"] = tempList
	
	return jsonify(result)
		
if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5002')
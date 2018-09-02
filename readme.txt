-----------------------------Standalone Setup
1) Pre-requisite setup
	1.1 Download and install Python 3.7 from https://www.python.org/.
	1.2 Download get-pip.py from https://bootstrap.pypa.io/get-pip.py. 
			and execute "python get-pip.py" if pip is not installed.
	1.3 Execute "pip install virtualenv" if isolated python enviroment is required.
	
	1.4 Execute "pip install flask flask-jsonpify flask-sqlalchemy flask-restful"
			in the local workstation or isolated enviroment 
			to setup the Flask framework enviroment.
			
	*Remark 
		- Ensure your local workstation has Internet connection

2) Run the server
	2.1 Execute "python server.py" to run the server.

3) Test the server
	3.1 Download and install Postman from https://www.getpostman.com/.
	3.2 Click the import button to import "SP - Full Stack Engineer.postman_collection.json".
	
----------------------------- Cloud Hosting
1) Send an email to shclai@gmail.com and/or shclai@hotmail.com, with the following details 48hrs in advance
	- Email Title : SP - Full Stack Engineer - API test
	- Email Content
		- Test date/time : DDMMYYYY / HH:MM:SS - HH:MM:SS

	Remark
		- Once the instance, hosting the application, in the cloud turned on, you will recieve email reply 
			with the IP address of the instance.
2) The instance, hosting the application, in the cloud will only be turned on during the period indicated in the email. 
	- IP address is only assigned upon turning on the instance in the Cloud.
	- This is to prevent cost overrun, cost of purchasing static IP, etc.

----------------------------- Docker Container
1) Update "server.py", line 366 to the following
	- app.run(host='0.0.0.0',port='5002')
2) Enter the following command to build the docker image
	- docker build -t python-flask -f dockerfile.python-flask .
3) Enter the following command to run the application in a docker container
	- docker run -p 5002:5002 python-flask

----------------------------- About
- server.py is an application to showcase API operation using Python Flask framework. The user stories and task list as follow

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
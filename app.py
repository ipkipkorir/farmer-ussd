from flask import Flask, request
import africastalking
import os

app = Flask(__name__)

username = "sandbox"
api_key = "acf6afa94b14298fcb067238ca5f99b8ecbc3d8df64f925ad9cf348663f3b84a"

africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods = ['POST', 'GET'] )
def ussd_callback():
	global response
	session_id = request.values.get("sessionId", None)
	service_code = request.values.get("serviceCode", None)
	phone_number = request.values.get("phoneNumber", None)
	text = request.values.get("text", "default")
	sms_phone_number = []
	sms_phone_number.append(phone_number)


	#USSD logic
	if text == "":
		#print main menu
		response = "CON Choose what to do: \n"
		response += "1. Check account details\n"
		response += "2. Check phone number\n"
		response += "3. Send me a cool message\n"

	elif text == "1":
		#print sub-menu 1
		response = "CON What would you like to check on your account?\n"
		response += "1. Account number\n"
		response += "2. Account balance\n"

	elif text == "2": 
		#print sub-menu 1
		response = "END Your phone number is {}" .format(phone_number)

	elif text == "3":
		try:

			#sending the sms
			sms_response = sms.send("Thank you for making this tutorial", sms_phone_number)
			print(sms_response)

		except Exception as e:
			#show us what went wrong
			print(f"Oops! we have a problem: {e}")
			
	elif text == "1*1":
		#USSD menus are split using *
		account_number = "123456789"
		response = "END Your account number is {}".format(account_number)

	elif text == "1*2":
		account_balance = "100,000.00"
		response = "END Your account balance is {}".format(account_balance)

	else:
		response = "END Invalid input. Try again."

	return response

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=os.environ.get("PORT"))


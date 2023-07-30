import random

number = '+14705983982'
code = 'AC110df7afdf0452781d47d99f001a72b1'
key = '5c5abb352d1a62f60f0ed04dd396b780'


from twilio.rest import Client


def generate_random_code():
    # Generate a random code of the specified length
    
    # print(code)
    # account_sid = code
    # auth_token = key
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     from_='+14705983982',
    #     to='+9779861397178',
    #     body='Your OTP verification code is '+ str(code)
    # )

    # print(message.sid)
    return code


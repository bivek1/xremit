import os
from twilio.rest import Client
from homepage.models import DefaultNumber, SMSSetting

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

defs = DefaultNumber.objects.first()
sm = SMSSetting.objects.first()

account_sid = sm.account_sid
auth_token = sm.auth_token
def TwilioOTPSMS(code, num):

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=str(code),
                        from_='+'+str(defs.number),
                        to='+'+str(num)
                    )

    print(message.sid)
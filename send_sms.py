
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC4794f18e08a357df60339cfaa88bca58'
auth_token = 'a15ad087ff31013ed093e90bc29d05ba'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     messaging_service_sid = 'MG5250661f2ab8628e6520b33f905daf4f',
                     to='+64272130734'
                 )

print(message.sid)



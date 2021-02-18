from twilio_credentials_private import cellphone, twilio_number, twilio_account, twilio_token
from twilio.rest import Client

account_sid = twilio_account
auth_token = twilio_token
client = Client(account_sid, auth_token)

message = client.messages.create(
    to = cellphone,
    from_ = twilio_number,
    body = "hello"
)

print(message.sid)
for sms in client.messages.list():
    print(sms.to)


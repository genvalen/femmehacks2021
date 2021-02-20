# from twilio_credentials import cellphone, twilio_number, twilio_account, twilio_token
# from twilio.rest import Client

# account_sid = twilio_account
# auth_token = twilio_token
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to = cellphone,
#     from_ = twilio_number,
#     body = "hello"
# )


# print(message.sid)
# for sms in client.messages.list():
#     print(sms.to)

# Debugger PIN: 404-199-630
# browser url
from flask import Flask, request, redirect
from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)
    # webhook
    # client.incoming_phone_numbers.list(phone_number=cellphone)[0].update(sms_url=SMS_URL)

    inb_msg = request.form['Body'].lower().strip()
    resp = MessagingResponse()
    if(inb_msg == "hi"):
        msg = resp.message("hi")
        msg.media("https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg")
    else:
        resp.message("else still hi, no image")
    return "hello"

if __name__ == "__main__":
    app.run(debug=True, host ="0.0.0.0")
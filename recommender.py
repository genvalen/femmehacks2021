from twilio import twiml
from twilio.rest import Client
from flask import Flask, request, redirect, send_file
import requests
from twilio.twiml.messaging_response import MessagingResponse

import json
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    category = ""
    size = ""
    responded = 0
    posCat = ['Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy']
    posSize = ['small', 'mid', 'big']
#     if 'quote' in incoming_msg:
#         # return a quote
#         r = requests.get('https://api.quotable.io/random')
#         if r.status_code == 200:
#             data = r.json()
#             quote = f'{data["content"]} ({data["author"]})'
#         else:
#             quote = 'I could not retrieve a quote at this time, sorry.'
#         msg.body(quote)
#         responded = True
#     if 'cat' in incoming_msg:
#         # return a cat pic
#         msg.media('https://cataas.com/cat')
#         responded = True
    if responded == 0:
        msg.body("Hi there! Which category do you want to donate to:'Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy'?")
    if incoming_msg in posCat:
        category = incoming_msg
        responded = responded + 1
        msg.body("Would you like to donate to a 'small', 'mid' or 'big' organization?")
    if incoming_msg in posSize and responded == 1:
        size = incoming_msg
        responded = responded + 1
        msg.body(get_org_recs('Environment', size))
    return str(resp)

# @app.route('/collect',  methods=['POST'])
# def collect():
#     memory = json.loads(request.form.get('Memory'))

#     answers = memory['twilio']['collected_data']['org_to_donate']['answers']

#     category = answers['category']['answer']
#     size = answers['size']['answer']

#     options = get_org_recs(category, size)
    
#     recs = options.get('title_rec', None)
    
#     message = (
#         f'Ok, you want to donate to a {size} sized organization in {category}.'
#         f' Here are some options: {recs}.'
#     )

#     return {
#         'actions': [
#             {'say': message},
#             {'listen': True},
#             {"remember" : options }
#         ]
#     } 

def get_org_recs(category, size):
    memory = json.loads(request.form.get('Memory'))
    filename = 'CLEAN_charity_data.csv'
    df = pd.read_csv(filename, header=0, sep=',',index_col=False, encoding='utf8',lineterminator='\n')
    
    df_cat = df.loc[df['category'] == category]
    df_size = df_cat.loc[df['size'] == size]
    df_sorted = df_size.sort_values('score', ascending=False)

    recomended_orgs = df_sorted['name'][0] + ', ' + df_sorted['name'][1]+ ', ' + df_sorted['name'][2]
    return recommended_orgs


# @app.route("/sms", methods=['GET', 'POST'])
# def incoming_sms():
#     """Send a dynamic reply to an incoming text message"""
#     # Get the message the user sent our Twilio number
#     body = request.values.get('Body', None)

#     # Start our TwiML response
#     resp = MessagingResponse()

#     # Determine the right reply for this message
#     if body == 'boo':
#         resp.message("Hi! which category do you want to donate to?")
#     elif body == 'bye':
#         resp.message("Goodbye")
# #     resp.message("Hi! which category do you want to donate to?")
#     return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio import twiml
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import numpy as np
import pandas as pd
import re

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    return send_file('start.json')

@app.route('/collect',  methods=['POST'])
def collect():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['org_to_donate']['answers']

    category = answers['category']['answer']
    size = answers['size']['answer']

    options = get_org_recs(category, size)
    
    recs = options.get('title_rec', None)
    
    message = (
        f'Ok, you want to donate to a {size} sized organization in {category}.'
        f' Here are some options: {recs}.\n\n Do you want more info about any of these titles Y/N?'
    )

    return {
        'actions': [
            {'say': message},
            {'listen': True},
            {"remember" : options }
        ]
    } 

@app.route('/get-tv-recs', methods=['GET'])
def get_org_recs(category, size):
    memory = json.loads(request.form.get('Memory'))
    filename = 'CLEAN_charity_data.csv'
    df = pd.read_csv(filename, header=0, sep=',',index_col=False, encoding='utf8',lineterminator='\n')
    
    df_cat = df.loc[df['column_name'] == category]
    df_size = df_cat.loc[df['column_name'] == size]
    df_sorted = df_size.sort_values('score', ascending=False)

    recomended_orgs = df_sorted['name'][0] + ', ' + df_sorted['name'][1]+ ', ' + df_sorted['name'][2]
    return { 'recs': recommended_orgs}


# @app.route("/sms", methods=['GET', 'POST'])
# def incoming_sms():
#     """Send a dynamic reply to an incoming text message"""
#     # Get the message the user sent our Twilio number
#     body = request.values.get('Body', None)

#     # Start our TwiML response
#     resp = MessagingResponse()

#     # Determine the right reply for this message
#     if body == 'hello':
#         resp.message("Hi!")
#     elif body == 'bye':
#         resp.message("Goodbye")

#     return str(resp)

if __name__ == "__main__":
    app.run(debug=True)




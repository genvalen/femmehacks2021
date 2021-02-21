from twilio import twiml
from twilio.rest import Client
from flask import Flask, request, redirect, send_file
import requests
from twilio.twiml.messaging_response import MessagingResponse

import pickle
import json
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    category = ""
    size = ""
    responded = False
    posCat = ['Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy']
    posSize = ['small', 'mid', 'big']
    print(incoming_msg)
    if (incoming_msg.lower() in posCat):
        category = incoming_msg
        msg.body("Would you like to donate to a 'small', 'mid' or 'big' organization?")
    if (incoming_msg in posSize):
        size = incoming_msg.lower()
        print(size)
        msg.body(get_org_recs(category, size))
        responded = True
    if not responded:
        msg.body("Hi there! Which category do you want to donate to:'Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy'?")
    return str(resp)


def get_org_recs(category, size):
    # memory = json.loads(request.form.get('Memory'))
    
    df_cat = df.loc[df['category'] == category]
    df_size = df_cat.loc[df['size'] == size]
    df_sorted = df_size.sort_values('score', ascending=False)
    a = df_sorted.iloc[0]['name'] + ", "
    b = df_sorted.iloc[1]['name'] + ", "
    c = df_sorted.iloc[2]['name'] + ""
    recomended_orgs = a + b + c
    return recomended_orgs


if __name__ == "__main__":
    # make csv into dataframe, pickle dataframe, then unpickle
    # this section will be updated when integrated with gcp storage
    input_file = 'CLEAN_charity_data.csv'
    pickled_file = 'charities_df.pickle'
    charities_df = pd.read_csv(input_file, header=0, sep=',',index_col=False, encoding='utf8',lineterminator='\n')
    charities_df.to_pickle(pickled_file)
    df = pd.read_pickle(pickled_file)


    app.run(debug=True)

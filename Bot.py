#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import requests
import base64
import time
import locale
import os 
from os import environ 


# In[2]:


api = environ['api']
api_secret = environ['api_secret']
api_bearer = environ['api_bearer']
accesstoken = environ['accesstoken']
accesssecrettoken = environ['accesssecrettoken']
cmcapi = environ['cmcapi']


# In[3]:


#authenticating to access the twitter API
auth=tweepy.OAuthHandler(api,api_secret)
auth.set_access_token(accesstoken,accesssecrettoken)
api=tweepy.API(auth)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': cmcapi,
}

session = requests.Session()
session.headers.update(headers)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
response = session.get(url)

while True:
    tweet = ''
    tweet2 = ''
    for i in range(10):
        cryptoprice = round((response.json()['data'][i]['quote']['USD']['price']), 2)
        price = response.json()['data'][i]['quote']['USD']['price']
        change = response.json()['data'][i]['quote']['USD']['percent_change_1h']
        valuechange = round(price - (price/(change/100+1) / 100), 2)
        if 'USD' in response.json()['data'][i]['symbol']:
            tweet = tweet + response.json()['data'][i]['symbol'] + ': $1' +'\n'
            continue
        if change > 0:
            add = response.json()['data'][i]['symbol'] + ': {}(+{}, {}%)'.format(locale.currency(cryptoprice, grouping=True), locale.currency(valuechange, grouping = True), round(change, 2)) + '\n'
            if len(tweet+add) > 280:
                tweet2 = tweet2 + add
            else:
                tweet = tweet + add
        else:
            add = response.json()['data'][i]['symbol'] + ': {}({}, {}%)'.format(locale.currency(cryptoprice, grouping=True), locale.currency(valuechange, grouping = True), round(change, 2)) + '\n'

            if len(tweet+add) > 280:
                tweet2 = tweet2 + add
            else:
                tweet = tweet + add
    print(tweet)
    api.update_status(tweet)
    if tweet2 != '':
        print(tweet2)
        api.update_status(tweet2)
    
    time.sleep(1800)

    tweet = 'Market Cap:\n\n'
    def human_format(num):
        num = float('{:.5g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '${} {}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'Mn', 'Bn', 'Tn'][magnitude])
    for i in range(10):
        tweet = tweet + response.json()['data'][i]['name'] + ': ' + human_format(response.json()['data'][i]['quote']['USD']['market_cap']) + '\n'
    print(tweet)
    api.update_status(tweet)
    time.sleep(1800)





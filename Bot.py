#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import requests
import base64
import bs4
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
import os 
from os import environ 


# In[2]:


binance_api_key = environ['binance_api_key']    #Enter your own API-key here
binance_api_secret = environ['binance_api_secret'] #Enter your own API-secret here

client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


api = environ['api']
api_secret = environ['api_secret']
api_bearer = environ['api_bearer']
accesstoken = environ['accesstoken']
accesssecrettoken = environ['accesssecrettoken']


# In[3]:


#authenticating to access the twitter API
auth=tweepy.OAuthHandler(api,api_secret)
auth.set_access_token(accesstoken,accesssecrettoken)
api=tweepy.API(auth)


# In[4]:


y = 0
listone = []
while y < 10:
    url = requests.get('https://www.coingecko.com/en')
    soup = bs4.BeautifulSoup(url.text, 'lxml')
    scrapedsymbol = soup.select('.d-lg-none.font-bold')[y].text
    scrapedsymbol = scrapedsymbol.rstrip("\n")
    scrapedsymbol = scrapedsymbol.strip("\n")
    y += 1
    listone.append(scrapedsymbol)


# In[31]:


locale.setlocale(locale.LC_ALL, 'en_US')
iteri = 0
percent = 0
lp = True
while True:
    tweetlist = []
    latestprice = client.get_all_tickers()
    for tick in listone:

        firsthalf = tick

        concat = firsthalf + 'USDT'
        
        if 'USD' in firsthalf:
            #print(firsthalf + ': $1')
            iteri += 1
            tweet = firsthalf + ': $1'
            tweetlist.append(tweet)
            continue

        if iteri < 10:
            a = client.get_all_tickers()
            x = 0
            for i in a:
                if a[x]['symbol'] == concat:
                    #print('If this is true')
                    #print(x)
                    p = round(float(a[x]['price']), 2)
                    #p = round(p, 2)
                    tweet = firsthalf + ': $' + str(p)
                    tweetlist.append(tweet)
                    break
                x += 1
                
            #api.update_status(final)
            iteri += 1
        else:
            #latestprice = client.get_all_tickers()
            x = 0
            for i in latestprice:
                if latestprice[x]['symbol'] == concat:
                    p = float(latestprice[x]['price'])
                    p = round(p, 2)
                    price = firsthalf + ': ' + locale.currency(p, grouping=True)
                    change = float(p) - float(a[x]['price'])
                    change = round(change, 4)
                    percent = round(change/float(a[x]['price']) * 100, 2)
                    if change > 0:
                        tweet = price + ',' + '(' + locale.currency(change, grouping=True) + ', +' + str(percent) + '%)'
                        tweetlist.append(tweet)
                    else:
                        tweet = price + ',' + '(' + locale.currency(change, grouping=True) + ', ' + str(percent) + '%)'
                        tweetlist.append(tweet)
                    break
                x += 1
                lp = False
    
    final = ''
    if lp == True:
        for tweet in tweetlist:
            final = final + '\n' + tweet
        #print(final)
        time.sleep(360)
        continue
    else:
        a = latestprice
        for tweet in tweetlist:
            final = final + '\n' + tweet
        print(final)
        #api.update_status(final)
        time.sleep(3600)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[5]:


#pip install tweepy


# In[6]:


import tweepy as tw


# In[7]:


consumer_key = 'TtUL61QbxZFf2mf6nGhswaC7u'
consumer_secret = 'rsBBMd5Gl8umwvgZtg2mTCAXTfWPZn8OXcrV6kXTrTWZ9kyCKX'
access_token = '2225673545-yEeOIRsKydNwtNQ7t7RmfSIHe9VCr92MI5n5YBu'
access_token_secret = 'iRbCQ56k7u0kPulG1RxGCWUAp5QfluNhdhZGDSfxyNC6g'


# In[8]:


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# In[9]:


public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)


# In[ ]:






# example from previous year
# performs the reccomendations for FaceDetection.py
# uses a factorisation machine model, popular technique
# incorporates features/factors about the user
# table with feature vectors of song and corresponding sentiment score that was assigned
# the nowplaying dataset doesn't include info about artists or titles of songs
# includes features like tempo, danceability, liveliness

# can use DL to extract features from the data, where features are not just text and easy to see
# can use it to extract features about the user, if have implicit feedback from user

# Imports

# In [1]:

import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pyfm import pylibfm
from pathlib import Path
from sklearn.model_selection import train_test_split
import pickle
import random

# Load Saved Model

# In [2]:

model = pickle.load(open("./FMModel/fittedmodel2.pickle","rb"))
v = DictVectorizer()

# In [3]:

# initialise trackid to feature dataset
trackidFeatDf = pd.read_csv('./nowPlayingRS/trackFeat.csv')
def getTrackidToFeature(trackId):
    '''
    Helper function for getUserReccomendation()
    Given a trackid returns its features
    '''
    global trackidFeatDf
    trackidRow = trackidFeatDf[trackidFeatDf['track_id'] == trackId]
    return [int(trackidRow['liveness'].values[0]*100),
            int(trackidRow['danceability'].values[0]*100),
            int(trackidRow['tempo'].values[0])]

# In [4]:

# init main df
path = Path('./nowplayingRS')
df = pd.read_csv(path/'nowplayingFinal.csv')
df = df.drop(columns=['Unnamed: 0'])
userTrackidsSentiment = None
def initUserTrackidsSentimentDf():
    '''
    This function initialises the dataframe that is later edited and fed to the model
    to get rating predictions for user.
    '''
    global userTrackidsSentiment,df
    track_ids = df['track_id'].unique()
    user_ids = ['1'] * len(track_ids)
    sentiment_scores = [0]*len(track_ids)
    userTrackidsSentiment = pd.DataFrame({'user_id':user_ids,'track_id':track_ids,'sentiment_score':sentiment_scores})

initUserTrackidsSentimentDf()

# In [24]:

def getRandomUserID():
    global df
    return random.choice(df['user_id'].unique())

# In [25]:

def setUserTrackidsSentimentDf(user_id,sentiment_score):
    '''
    Helper function of getUserReccomendation()
    Resets the user_id and sentiment_score in userTrackidsSentiment dataframe
    '''
    global userTrackidsSentiment
    userTrackidsSentiment['user_id'] = str(user_id)
    userTrackidsSentiment['sentiment_score'] = sentiment_score

# In [49]:

def getNBestReccomendationTabel(n,preds):
    '''
    Helper function of getNBestRTrackid()
    The function will return you a table
    '''
    global userTrackidsSentiment
    userTrackidsSentiment['rating'] = preds
    nBestRowsDf = userTrackidsSentiment.nlargest(n,'rating')
    return nBestRowsDf

# In [27]:

def getNBestTrackid(n,predRatings):
    '''
    Helper function for getUserReccomendations()
    Given a predRatings and number of desired reccomendations, it returns the top 5 track_id
    '''
    nBestRowsDf = getNBestReccomendationTabel(n,predRatings)
    return nBestRowsDf['track_id'].values

# In [76]:

recTrackObjs = None
currentUserId = None
def removePreviousRecommendation():
    global userTrackidsSentiment
    trackIds = [objs['track_id'] for objs in recTrackObjs]
    userTrackidsSentiment = (userTrackidsSentiment[~userTrackidsSentiment['track_id'].isin(trackIds)])

# In [77]:

def getUserReccomendation(user_id,sentiment_score):
    '''
    Given a user_id (Does not have to be in the database) and sentiment_score
    Returns trackObject [{'trackId':..., 'features':...,}]
    '''
    global currentUserId, recTrackObjs
    if recTrackObjs != None and currentUserId==user_id:
        removePreviousRecommendation()
    else:
        initUserTrackidsSentimentDf()
    setUserTrackidsSentimentDf(user_id,sentiment_score)

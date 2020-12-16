
# example of student work from previous year 
# context aware reccomender system
# using sentiment or emotions for music reccomendations
# using nowplaying dataset
# used deep learning for feature extraction
# used video feed to try to learn to detect emotion convolutional neural network (CNN)
# this extracts features and uses as emotion as sentiment (not neccessarily right?)
# used to figure out what mood the user is in for what they want to hear and also for if they like something, i think
# can just use this for a certain aspect of the data, here just to learn the context, the mood the user is in
# we shouldn't mix sentiment and emotion
# here they have performed sentiment analysis on the emotions to understand where the user fits in on a scale

# In [1]:

import numpy as np
import argparse
import imutils
import time
import cv2
from pathlib import Path
from fastai.vision import *

# In [2]:

args = {"model": './FaceDetectionModel/res10_300x300_ssd_iter_140000.caffemodel',
        "prototxt": './FaceDetectionModel/deploy.prototxt.txt',
        "confidence": 0.5,
        "image": './FaceDetectionModel/iron_chic.jpg',
        "emotion": ['ANGRY', 'DISGUST', 'FEAR', 'HAPPY', 'NEUTRAL', 'SAD', 'SURPRISE']}

# Emotion Recognition Model

# In [3]:

learn = load_learner('./FaceDetectionModel')

# In [4]:

# test_img = open_image(args['image'])
# x = learn.predict(test_img)
# x[1].item()

# In [5]:

def getStringEmotion(x):
    '''
    Helper function for getROIEmotion()
    Returns the emotion string that maps from pred tensor to args
    '''
    index = x[1].item()
    return args['emotion'][index]

# In [6]:

def getRoiEmotion(roi):
    '''
    Helper function for getFaceROI()
    Returns the emotion of string type in the ROI
    '''
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    cv2.resize(roi,(255,255))
    roi = Image(pil2tensor(roi, dtype=np.float32).div_(255))
    x = learn.predict(roi)
    roiEmotion = getStringEmotion(x)
    return roiEmotion

# Face Localisation model

# In [7]:

net = cv2.dnn.readNetFromCaffe(args["prototxt"],args["model"])

# In [8]:

image = cv2.imread(arge["image"])
(h,w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0,
        (300,300),(104.0,177.0,123.0))

# In [9]:

# pass the blob through the network and obtain the detections and predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

# In [10]:

def getRoi(frame,left,top,right,bottom):
    '''

    '''
    pass

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup as bs
import re,string

travel_train = pd.read_csv('travel.csv')
diy_train    = pd.read_csv('diy.csv')
bio_train    = pd.read_csv('biology.csv')
cook_train   = pd.read_csv('cooking.csv')
crypt_train  = pd.read_csv('crypto.csv')
robot_train  = pd.read_csv('robotics.csv')

uri_re = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
def remove_url(content):
    if content:
        soup = bs(content, "html.parser")
        # Stripping all <code> tags with their content if any
        if soup.code: soup.code.decompose()
        #remove html tags
        text = soup.get_text()
        #replace all unwanted characters with blank
        return  re.sub(uri_re," ",text)
    else:
        return ""


def clean_text(content):
    #lowercasing the text
    text = content.lower()
    # Removing non ASCII chars
    text = re.sub(r'[^\x00-\x7f]',r' ',text)
    # Removing (replacing with empty spaces actually) all the punctuations
    text = re.sub("["+string.punctuation+"]", " ", text)
    #splitting into words
    words=text.split()
    #removing the stop words in the text
    stop_word=set(stopwords.words('english'))
    words=list(word for word in words if not word in stop_word)
    words=[word for word in words if len(word)>1 ]
    return ( " ".join(words) )


all_files=[travel_train, diy_train, bio_train, cook_train, crypt_train, robot_train]
for a_file in all_files:
    a_file['content'] = a_file['content'].map(remove_url)
    a_file['title']   = a_file['title'].map(clean_text)
    a_file['content'] = a_file['content'].map(clean_text)
    
    # From a string sequence of tags to a list of tags
    a_file["tags"] = a_file["tags"].map(lambda x: x.split())

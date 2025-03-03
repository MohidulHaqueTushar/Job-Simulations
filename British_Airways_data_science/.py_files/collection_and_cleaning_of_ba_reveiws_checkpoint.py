# -*- coding: utf-8 -*-
"""collection_and_cleaning-of_BA-reveiws-checkpoint.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jV-Dc2uz_x1n0RZvM5_WlFnDEh2SQKyw

# Data Collection
  - Web scrapping from the website [Skytrax](https://www.airlinequality.com/airline-reviews/british-airways), clean, and analysis.
"""

# imports necessary modules

import os
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import datetime as dt

from wordcloud import WordCloud, STOPWORDS

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# collect all reviews, ratings stars, date, reviewer country
reviews, stars, date, country  = [], [], [], []

for i in range(1, 36):
    page = requests.get(f"https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/?sortby=post_date%3ADesc&pagesize=100")

    soup = BeautifulSoup(page.content, "html5")

    for item in soup.find_all("div", class_="text_content"):
        reviews.append(item.text)

    for item in soup.find_all("div", class_ = "rating-10"):
        try:
            stars.append(item.span.text)
        except:
            print(f"Error on page {i}")
            stars.append("None")

    #date
    for item in soup.find_all("time"):
        date.append(item.text)

    #country
    for item in soup.find_all("h3"):
        country.append(item.span.next_sibling.text.strip(" ()"))

# total reviews extracted
len(reviews)

# total reviewer country
len(country)

# total star length
len(stars)

# total date
len(date)

# fix the length of stars
stars = stars[:3500]
len(stars)

#create  a dataframe from these collected lists of data
df = pd.DataFrame({"reviews":reviews,"stars": stars, "date":date, "country": country})

# first five rows
df.head()

df.shape

# export the data in csv format
df.to_csv("data/BA_reviews.csv")

"""## Data Cleaning"""

# import data
df = pd.read_csv("data/BA_reviews.csv", index_col=0)

df.head()

# column which mentions if the user is verified or not
df['verified'] = df.reviews.str.contains("Trip Verified")

df['verified']

#extract the column of reviews into a separate dataframe and clean it for semantic analysis
#for lemmatization of words we will use nltk library
lemma = WordNetLemmatizer()
import nltk
nltk.download('stopwords')
# Download the 'wordnet' dataset
nltk.download('wordnet')


reviews_data = df.reviews.str.strip("✅ Trip Verified |")

#create an empty list to collect cleaned data corpus
corpus =[]

#loop through each review, remove punctuations, small case it, join it and add it to corpus
for rev in reviews_data:
    rev = re.sub('[^a-zA-Z]',' ', rev)
    rev = rev.lower()
    rev = rev.split()
    rev = [lemma.lemmatize(word) for word in rev if word not in set(stopwords.words("english"))]
    rev = " ".join(rev)
    corpus.append(rev)

# add the corpus to the original dataframe
df['corpus'] = corpus

df.head()

df.dtypes

# convert the date to datetime format
df.date = pd.to_datetime(df.date, format='mixed')

df.date.head()

#check for unique ratings
df.stars.unique()

# Convert the 'stars' column to string type before using .str accessor
df.stars = df.stars.astype(str).str.strip("\n\t\t\t\t\t\t\t\t\t\t\t\t\t")

df.stars.value_counts()

# drop the rows where the value of ratings is None
df.drop(df[df.stars == "None"].index, axis=0, inplace=True)

#check the unique values again
df.stars.unique()

# checking null value on all dataset
df.isnull().value_counts()

df.country.isnull().value_counts()

# drop the rows using index where the country value is null
df.drop(df[df.country.isnull() == True].index, axis=0, inplace=True)

df.shape

#resetting the index
df.reset_index(drop=True)

# export the cleaned data
df.to_csv("data/cleaned-BA-reviews.csv")


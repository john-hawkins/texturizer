# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

"""
    texturizer.topics: Common Topic Features

    Simple pattern matching to generate features for very common topics for text data.
    We have focused on topics that are common in media, commentary and diacussion by
    the general public.  
    The goal with these features is to provide a count of words which are 
    unambigously related to a specific topic.

    NOTE: That the words in these sets have been deliberately selected to be a set 
          that are less likely to match false positives. In other words they are 
          generally only used when talking about that specific topic, or when talking
          using metaphor or analogy.
"""


########################################################################################
resource_package = __name__

def load_word_list(filename):
    """
    Utility function to load topic vocab word lists for pattern matching. 
    """
    _path = '/'.join(('data', filename))
    rawd = pkg_resources.resource_string(resource_package, _path)
    word_list = str(rawd).split('\n')
    _list = [i for i in word_list if i]
    return _list

########################################################################################
religion_list = load_word_list('religion.dat')
pattern_start = "\\bchristi|\\bislam|\\b"
religion_pat = pattern_start  + ( "\\b|\\b".join(religion_list) ) + "\\b"
religion_re = re.compile(religion_pat)

politics_list = load_word_list('politics.dat')
pattern_start = "\\bpoliti|\\b"
politics_pat = pattern_start + ( "\\b|\\b".join(politics_list) ) + "\\b"
politics_re = re.compile(politics_pat)

sex_list = load_word_list('sex.dat')
pattern_start = "\\bsex[^t][^ *]\\b|\\b"
sex_pat = pattern_start + ( "\\b|\\b".join(sex_list) ) + "\\b"
sex_re = re.compile(sex_pat)

ethnicity_list = load_word_list('ethnicity.dat')
pattern_start = "\\bethn|\\b"
ethno_pat = pattern_start + ( "\\b|\\b".join(ethnicity_list) ) + "\\b"
ethno_re = re.compile(ethno_pat)

health_list = load_word_list('health.dat')
pattern_start = "\\bhealth|\\b"
health_pat = pattern_start + ( "\\b|\\b".join(health_list) ) + "\\b"
health_re = re.compile(health_pat)

econo_list = load_word_list('economics.dat')
pattern_start = "\\becono|\\bfinan|\\b"
econo_pat = pattern_start + ( "\\b|\\b".join(econo_list) ) + "\\b"
econo_re = re.compile(econo_pat) 
 
sports_list = load_word_list('sports.dat')
pattern_start = "\\bathlet\\b|\\b"
sport_pat = pattern_start + ( "\\b|\\b".join(sports_list) ) + "\\b"
sport_re = re.compile(sport_pat)

arts_list = load_word_list('arts.dat')
pattern_start = "\\bartist|\\b"
arts_pat = pattern_start + ( "\\b|\\b".join(arts_list) ) + "\\b"
arts_re = re.compile(arts_pat)
  
family_list = load_word_list('family.dat')
pattern_start = "\\bfamil\\b|\\b"
family_pat = pattern_start + ( "\\b|\\b".join(family_list) ) + "\\b"
family_re = re.compile(family_pat)

love_list = load_word_list('love.dat')
pattern_start = "\\bromanc\\b|\\b"
love_pat = pattern_start + ( "\\b|\\b".join(love_list) ) + "\\b"
love_re = re.compile(love_pat)

crime_list = load_word_list('crime.dat')
pattern_start = "\\bcrimina|\\b"
crime_pat = pattern_start + ( "\\b|\\b".join(crime_list) ) + "\\b"
crime_re = re.compile(crime_pat)

travel_list = load_word_list('travel.dat')
pattern_start = "\\btravel|\\b"
travel_pat = pattern_start + ( "\\b|\\b".join(travel_list) ) + "\\b"
travel_re = re.compile(travel_pat)

food_list = load_word_list('food.dat')
pattern_start = "\\b|\\b"
food_pat = pattern_start + ( "\\b|\\b".join(food_list) ) + "\\b"
food_re = re.compile(food_pat)

########################################################################################
def add_text_topics_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_topic_features(rez, col)
    return rez

########################################################################################
def add_topic_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for profanities.
    """

    def prof_features(x, col):
        religion_wds = 0
        sex_wds = 0
        politics_wds = 0
        ethno_wds = 0
        econo_wds = 0
        health_wds = 0 
        sport_wds = 0 
        arts_wds = 0 
        family_wds = 0 
        love_wds = 0 
        crime_wds = 0 
        if x[col]!=x[col]:
            sex_wds = 0
        else:
            text = (x[col].lower())
            religion_wds = len(religion_re.findall(text))
            politics_wds = len(politics_re.findall(text))
            sex_wds = len(sex_re.findall(text))
            ethno_wds = len(ethno_re.findall(text))
            econo_wds = len(econo_re.findall(text))
            health_wds = len(health_re.findall(text))
            sport_wds = len(sport_re.findall(text))
            arts_wds = len(arts_re.findall(text))
            family_wds = len(family_re.findall(text))
            love_wds = len(love_re.findall(text))
            crime_wds = len(crime_re.findall(text))
        return religion_wds, politics_wds, sex_wds, ethno_wds, econo_wds, health_wds, sport_wds, arts_wds, family_wds, love_wds, crime_wds

    df[[ col+'_religion', col+'_politics', col+'_sex', col+'_ethnicity', col+'_economics', col+'_health', col+'_sport', col+'_arts', col+'_family', col+'_love', col+'_crime']] = df.apply(prof_features, col=col, axis=1, result_type="expand")
    return df
 

# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list

"""
    texturizer.topics: Common Topic Features

    Simple pattern matching to generate features for very common topics for text data.
    We have focused on topics that are common in both traditional and social media, 
    as well as commentary and discussion by the general public.
  
    The goal with these features is to provide a count of words which are 
    unambigously related to a specific topic.

    NOTE: That the words in these sets have been deliberately selected to be a set 
          that are less likely to match false positives. In other words they are 
          generally only used when talking about that specific topic, or when talking
          using metaphor or analogy.
"""

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
def add_text_topics_features(df, columns, type="flag"):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        if type=="count":
            rez = add_topic_features(rez, col)
        else:
            rez = add_topic_indicators(rez, col)
    return rez

########################################################################################
def add_topic_features(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the text matches for topic keywords.
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
        travel_wds = 0 
        food_wds = 0 
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
            travel_wds = len(travel_re.findall(text))
            food_wds = len(food_re.findall(text))
        return religion_wds, politics_wds, sex_wds, ethno_wds, econo_wds, health_wds, sport_wds, arts_wds, family_wds, love_wds, crime_wds, travel_wds, food_wds

    df[[ col+'_religion', col+'_politics', col+'_sex', col+'_ethnicity', col+'_economics', col+'_health', col+'_sport', col+'_arts', col+'_family', col+'_love', col+'_crime', col+'_travel', col+'_food']] = df.apply(prof_features, col=col, axis=1, result_type="expand")
    return df

########################################################################################
def add_topic_indicators(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match for top indicators.
    """ 
    df[ col+'_religion' ] = 0
    df.loc[(df[col].notnull()) & (df[col].str.contains(religion_pat)), col+'_religion' ] = 1
    df[ col+'_politics' ] = 0
    df.loc[(df[col].notnull()) & (df[col].str.contains(politics_pat)), col+'_politics' ] = 1
    df[ col+'_sex' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(sex_pat)), col+'_sex' ]=1
    df[ col+'_ethnicity' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(ethno_pat)), col+'_ethnicity' ]=1
    df[ col+'_economics' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(econo_pat)), col+'_economics' ]=1
    df[ col+'_health' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(health_pat)), col+'_health' ]=1
    df[ col+'_sport' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(sport_pat)), col+'_sport' ]=1
    df[ col+'_arts' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(arts_pat)), col+'_arts' ]=1
    df[ col+'_family' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(family_pat)), col+'_family' ]=1
    df[ col+'_love' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(love_pat)), col+'_love' ]=1
    df[ col+'_crime' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(crime_pat)), col+'_crime' ]=1
    df[ col+'_travel' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(travel_pat)), col+'_travel' ]=1
    df[ col+'_food' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(food_pat)), col+'_food' ]=1

    return df


# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import re

emoticons = { "smile":[":-)","(-:",":)","(:"], 
              "wink":[";-)","(-;",";)","(;"], 
              "think":[":^)","(^:"], 
              "laugh":[":-D",":D"], 
              "tongue":[":-P",":P"], 
              "sad":[":-(",":(","):",")-:"], 
              "crying":[":’-(",")-`:",":'-(",")-':"], 
              "happycry":[":’-)","(-`:",":’)","(`:",":'-)","(-':"]
            }

fwd_regex = "[:;]['’`]{0,1}[-=^]{0,2}[DP@*\\|/()<>{}\[\]]{1,2}"
fwd_re = re.compile(fwd_regex)
bck_regex = "[@*\\|/()<>{}\[\]]{1,2}[-=^]{0,2}['’`]{0,1}[:;]"
bck_re = re.compile(bck_regex)

"""
    texturizer.emoticons: Emoticon Recognition Text Features
 
    The functions in this library will add columns to a dataframe that indivate
    whether there are emoticons in certain columns of text, and whether those
    emoticons represent one of the more common emotions.

    NOTE: In developing these regexes I have deliberately ignored certain emoticons 
     because of the likelihood of false positive matches in text containing brackets
     For example emoticons: 8) or (B will not be matched.

    To avoid matching characters inside document markup language tags there is a 
    rudimentary regex based tag removal. 
"""


########################################################################################
def add_text_emoticon_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        Add features that detect the presence of emoticons.
    """
    rez = df.copy()
    if len(columns) == 0:
        columns = get_text_column_names(df)
    for col in columns:
        rez = add_emoticon_features(rez, col)
    return rez


########################################################################################
def add_emoticon_features(df, col):
    """
        Given a pandas dataframe and a column name.
        Check for emoticons in the column and add a set of features
        that indicate both the presence and emotional flavour of the emoticon.
    """
    def cal_features(x, col):
        emo_match = 0 
        smiley = 0 
        wink = 0 
        sad = 0
        happycry = 0
        laugh = 0
        tongue = 0
        crying = 0
        if x[col]==x[col]:
            text = remove_urls_and_tags(x[col].lower())
            matches = fwd_re.findall(text)
            bck_matches = bck_re.findall(text)
            if len(matches)>0 or len(bck_matches)>0:
                matches.extend(bck_matches)
                emo_match = len(matches) 
                if set(matches).intersection(emoticons['smile']):                
                    smiley = 1
                if set(matches).intersection(emoticons['crying']):                
                    crying = 1
                if set(matches).intersection(emoticons['wink']):                
                    wink = 1
                if set(matches).intersection(emoticons['sad']):                
                    sad = 1
                if set(matches).intersection(emoticons['laugh']):                
                    laugh = 1
                if set(matches).intersection(emoticons['tongue']):                
                    tongue = 1
                if set(matches).intersection(emoticons['happycry']):                
                    happycry = 1
        return emo_match, smiley, wink, sad, crying, tongue, laugh, happycry

    df[[col+'_emoticons', col+'_emo_smiley', col+'_emo_wink', col+'_emo_sad', col+'_emo_cry', col+'_emo_tongue', col+'_emo_laugh', col+'_emo_happycry']] = df.apply(cal_features, col=col, axis=1, result_type="expand")

    return df

def remove_urls_and_tags(text):
    """
        Necessary to avoid common false positive emoticon matches
    """
    patterns = ["https?://[-._a-z0-9A-Z]*","</?[a-zA-Z]* ?[a-zA-Z'=.]* ?/?>","\\[tnrf]"]
    new_text = text
    for p in patterns:
        new_text = re.sub(p, ' ', new_text)
    return new_text

########################################################################################
def null_tolerant_len(x):
    if x != x:
        return 0
    else:
        return len(x)

########################################################################################
def get_text_column_names(df):
    rez = []
    return rez


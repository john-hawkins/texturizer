# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import math
import os
import re

"""
    texturizer.profanity: Profanity feature flags

    Simple word matching to generate features for common profanities, insults and slurs.

    I have generalised towards words that are unambiguously intended to insult or offend.
    There will therefore be some forms that are not cpatured because they have alternative
    uses in general English. For example: "whore", "spick", or "wog" are all words that 
    have legitimate applications where offence is not the intended purpose of usage.

    NOTE: That these have been deliberately reduced to a set that are more likely to be 
          encountered in modern Australian spoken language or internet comments.

"""

########################################################################################
 
pattern_start = "[ '(\"]fuck[^ ]*|[ '(\"]cunt[^ ]*[ .,?;:']|[- '(\"]"
hard_profanity_list = ["cockhead","bastard","bitch","shit","piss","piss-off","pissing","piss-poor","cocksucker", "cocksucka", "shits","shitloads", "shitfaced", "shithead", "shitlist"]
hard_pat = pattern_start  + ( "[ .,?!;:'\"]|[- '(\"]".join(hard_profanity_list) ) + "[ .,?;:']"
hard_re = re.compile(hard_pat)

mild_profanity_list = ["bugger","bloody","crap","damnit","sod","goddamn","wanker","bollocks","bullshit"]

non_profanity_list = ["fiddlesticks","blimey" ,"zounds","gad","gadzooks","gosh","golly","darn","tarnation","dang","jiminy","drat","crikey","doggone","heck","gee","gorblimey","jeez","jeepers","jeepers-creepers"]

insult_list = ["twat", "moron", "dweeb", "cretin", "idiot", "dickhead", "cockhead", "cocksucker", "cocksucka", "cuck", "faggot", "poofter", "poofta", "cuntboy", "fuckwit", "arsehole", "bastard", "bitch", "douchebag", "douchnozzle", "shitgibbon", "cockwaffle", "shithead", "twatwaffle", "fucktrumpet", "pisswizard","fuckface", "fuckhead", "sissy", "slut", "soyboy", "soy-boy", "shitfaced", "shithead", "shitbag", "shitstain", "shithole","dumbass","motherfucker", "dumbfuck", "fuckknuckle", "fucknuckle", "motherfucka", "muthafucka", "redneck", "red-neck", "whitetrash", "white-trash", "trailertrash", "trailer-trash"]

slur_list = ["abo","abbo","boong", "chinaman", "chonky", "curry-muncher", "darky","darkey","darkie", "gook", "guizi", "gweilo", "half-breed", "nigger", "raghead", "rag-head", "sandnigger", "sand-nigger", "sambo", "slanteye", "slant-eye", "slopehead", "slope-head","towelhead", "towel-head","spearchucker","spear-chucker", "wigger", "whigger", "wigga", "wop"] 

masked_pat = "\\bf[*%$#@c?]{2}k|\\bs[*%$#@h?1!4]{2}t|\\bc[*%$#@n]{2}t|\\b@$$|\\b$h1t|\\bb!tch|\\bbi\+ch|\bc0ck|\\bl3itch\\b|\\bp\*ssy\\b|\\bdik\\b"
masked_re = re.compile(masked_pat)

########################################################################################
def add_text_profanity_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_profanity_features(rez, col)
    return rez

########################################################################################
def add_profanity_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for profanities.
    """

    def prof_features(x, col):
        hard_profanity = 0
        mask_profanity = 0
        contains_insult = 0
        mild_profanity = 0
        non_profanity = 0
        contains_slur = 0
        if x[col]!=x[col]:
            mild_profanity = 0
        else:
            text = (x[col].lower())
            word_array = text.split()
            hard_profanity = len(hard_re.findall(text))
            mask_profanity = len(masked_re.findall(text))
            if set(mild_profanity_list).intersection(word_array):
                mild_profanity = 1
            if set(non_profanity_list).intersection(word_array):
                non_profanity = 1
            if set(insult_list).intersection(word_array):
                contains_insult = 1
            if set(slur_list).intersection(word_array):
                contains_slur = 1
        return hard_profanity, mask_profanity, mild_profanity, non_profanity, contains_insult, contains_slur

    df[ get_profanity_col_list(col) ] = df.apply(prof_features, col=col, axis=1, result_type="expand")

    return df
 

########################################################################################
def get_profanity_col_list(col):
    return [ col+'_profane_hard', col+'_profane_masked', col+'_profane_mild', col+'_profane_non', col+'_insult', col+'_slur' ]


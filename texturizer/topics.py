# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import math
import os
import re

"""
    texturizer.topics: Common Topic Features

    Simple pattern matching to generate features for very common topics that come up 
    when building models for sentiment or document classification. These features will
    contain the count of words which are unambigously related to a specific topic.

    NOTE: That these have been deliberately reduced to a set that are more likely to be 
          encountered in modern Australian spoken language or internet comments.
"""

########################################################################################

pattern_start = "[ '(\"]christ[^ ]*[ .,?;:']|[ '(\"]islam[^ ]*[ .,?;:']|[ '(\"]"
religion_list = ["jesus","christ","god","christians", "islam", "islamic","jew","jewish", "judaism", "holy", "church", "ashram", "budhha", "hindu", "jehovah", "allah", "religious","religion", "pious","godly", "spiritual", "muslim", "infidel", "shinto", "apostate", "messiah", "theology", "sacred", "scripture","missionary","hinduism","buddhism","rabbi","koran","synagogue","torah","protestant","spirituality","protestantism","catholic","catholicism","presbytery","blasphemy","blaspheme","krishnaism","krishna","mormon","theism","monotheism","poltheism","polytheist","polytheistic","abrahamic", "baptize", "bible-basher", "pentecostal", "pentecostalism", "god–fearing" ]
religion_pat = pattern_start  + ( "[ .,?!;:'\"]|[- '(\"]".join(religion_list) ) + "[ .,?;:']"
religion_re = re.compile(religion_pat)

pattern_start = "[ '(\"]politic[^ ]*[ .,?;:']|[ '(\"]"
politics_list = ["federal","politics","election","senator","government","democratic","totalitarian","democracy","political", "policy", "lobbyist", "governor", "mayor", "council", "capitalism", "communism", "socialism", "capitalist", "socialist", "communist", "republic", "republican", "libertarian", "leftwing", "left-wing", "rightwing", "right-wing","demagogue","gerrymander", "ideology", "bipartisan", "caucus", "politicise", "politically", "politicking", "sociopolitical","dictator","dictatorship","monarchy","democrat","congress"] 
politics_pat = pattern_start + ( "[ .,?!;:'\"]|[- '(\"]".join(politics_list) ) + "[ .,?;:']"
politics_re = re.compile(politics_pat)

pattern_start = "[ '(\"]sex[^ ]*[ .,?;:']|[ '(\"]"
sex_list = ["sex", "sexuality", "homosexuality", "homosexual", "heterosexuality", "heterosexual", "bisexuality","bisexual","orgasm","g-spot","masturbation","masturbate","pornography","porn","whore","prostitute","prostitution","oral-sex","cunnilingus","felatio","vagina","penis","anal-sex", "doggy-style", "kinky", "vajayjay", "punani", "furburger"]
sex_pat = pattern_start + ( "[ .,?!;:'\"]|[- '(\"]".join(sex_list) ) + "[ .,?;:']"
sex_re = re.compile(sex_pat)

pattern_start = "[ '(\"]ethn[^ ]*[ .,?;:']|[ '(\"]"
ethnicity_list = ["african", "african-american", "aboriginal", "arabian", "hispanic", "east-asian","asian", "caucasian", "european", "indian", "islander", "maori", "afro-caribbean", "ethnicity", "ethnic", "racism", "racial"]
ethno_pat = pattern_start + ( "[ .,?!;:'\"]|[- '(\"]".join(ethnicity_list) ) + "[ .,?;:']"
ethno_re = re.compile(ethno_pat)

pattern_start = "[ '(\"]health[^ ]*[ .,?;:']|[ '(\"]"
health_list = ["health", "vaccine", "vaccinate", "medication", "medications", "physician", "hospital", "diet", "vegan", "vegetarian", "allergy", "allergic", "autism", "medicine", "medical", "healthcare", "bacteria", "virus", "disease", "surgery", "surgical", "infection", "symptoms", "doctor", "pharmacy", "vitamins"]
health_pat = pattern_start + ( "[ .,?!;:'\"]|[- '(\"]".join(health_list) ) + "[ .,?;:']"
health_re = re.compile(health_pat)

pattern_start = "[ '(\"]econo[^ ]*[ .,?;:']|[ '(\"]financ[^ ]*[ .,?;:']|[ '(\"]"
econo_list = ["finance", "money", "savings", "investment", "wages", "salary", "superannuation", "finances", "financial", "monetary", "taxation", "taxes", "accounting", "profit", "profits", "roi", "ebitda", "corporation"]
econo_pat = pattern_start + ( "[ .,?!;:'\"]|[- '(\"]".join(econo_list) ) + "[ .,?;:']"
econo_re = re.compile(econo_pat) 
 
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
        if x[col]!=x[col]:
            sex_wds = 0
        else:
            text = (x[col].lower())
            word_array = text.split()
            religion_wds = len(religion_re.findall(text))
            politics_wds = len(politics_re.findall(text))
            sex_wds = len(sex_re.findall(text))
            ethno_wds = len(ethno_re.findall(text))
            econo_wds = len(econo_re.findall(text))
            health_wds = len(health_re.findall(text))
        return religion_wds, politics_wds, sex_wds, ethno_wds, econo_wds, health_wds

    df[[ col+'_religion', col+'_politics', col+'_sex', col+'_ethnicity', col+'_economics', col+'_health']] = df.apply(prof_features, col=col, axis=1, result_type="expand")
    return df
 

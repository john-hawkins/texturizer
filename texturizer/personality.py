# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list
 
"""
    texturizer.literacy: Personality trait feature flags

    This module performs word or phrase matching to generate features 
    that can be indicative of personailuty traits in a writer or speaker.

    Some ideas taken from these articles

    https://www.scientificamerican.com/article/you-are-what-you-say/

    https://hbr.org/2011/12/your-use-of-pronouns-reveals-your-personality
"""

########################################################################################

reasoning_list = load_word_list('reasoning.dat') 
pattern_start = "\\b"
reasoning_pat = pattern_start  + ( "\\b|\\b".join(reasoning_list) ) + "\\b"
reasoning_re = re.compile(reasoning_pat)

nuance_list = load_word_list('nuance.dat') 
pattern_start = "\\b"
nuance_pat = pattern_start  + ( "\\b|\\b".join(nuance_list) ) + "\\b"
nuance_re = re.compile(nuance_pat)

explain_list = load_word_list('explain.dat') 
pattern_start = "\\b"
explain_pat = pattern_start  + ( "\\b|\\b".join(explain_list) ) + "\\b"
explain_re = re.compile(explain_pat)

singular_pat = "\\bi\\b|\\bme\\b|\\bmyself\\b|\\bmy\\b|\\bmine\\b"
singular_re = re.compile(singular_pat)

plural_pat = "\\bwe\\b|\\bus\\b|\\bour\\b|\\bourselves\\b"
plural_re = re.compile(plural_pat)

########################################################################################
def add_text_personality_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the personality trait features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_personality_features(rez, col)
    return rez

########################################################################################
def add_personality_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for personality traits.
    """

    def trait_features(x, col):
        reasoning = 0
        explain = 0
        nuance = 0
        singular = 0
        plural = 0
        if x[col]!=x[col]:
            reasoning = 0
        else:
            text = (x[col].lower())
            reasoning = len(reasoning_re.findall(text))
            explain = len(explain_re.findall(text))
            nuance = len(nuance_re.findall(text))
            singular = len(singular_re.findall(text))
            plural = len(plural_re.findall(text))
        return reasoning, explain, nuance, singular, plural

    df[[ col+'_reason', col+'_explain', col+'_nuance', col+'_singular', col+'_plural' ]] = df.apply(trait_features, col=col, axis=1, result_type="expand")

    return df
 

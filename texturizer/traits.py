# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_pattern
 
"""
    texturizer.traits: Personality trait feature flags

    This module performs word or phrase matching to generate features 
    that can be indicative of personailuty traits in a writer or speaker.

    Some ideas taken from these articles

    https://www.scientificamerican.com/article/you-are-what-you-say/

    https://hbr.org/2011/12/your-use-of-pronouns-reveals-your-personality
"""

########################################################################################

reasoning_pat = load_word_pattern('reasoning.dat')
reasoning_re = re.compile(reasoning_pat)

nuance_pat = load_word_pattern('nuance.dat')
nuance_re = re.compile(nuance_pat)

explain_pat = load_word_pattern('explain.dat')
explain_re = re.compile(explain_pat)

singular_pat = "\\bi\\b|\\bme\\b|\\bmyself\\b|\\bmy\\b|\\bmine\\b"
singular_re = re.compile(singular_pat)

plural_pat = "\\bwe\\b|\\bus\\b|\\bour\\b|\\bourselves\\b"
plural_re = re.compile(plural_pat)

quotation_pat = "\"[ a-zA-Z0-9.,?!:;']*\""

########################################################################################
def add_text_trait_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the personality trait features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_trait_counts(rez, col)
    return rez

########################################################################################
def add_trait_counts(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the number of keyword matches for each trait
    """
    df[col+'_reason']=df[col].str.count(reasoning_pat, flags=re.IGNORECASE)
    df[col+'_explain']=df[col].str.count(explain_pat, flags=re.IGNORECASE)
    df[col+'_nuance']=df[col].str.count(nuance_pat, flags=re.IGNORECASE)
    df[col+'_singular']=df[col].str.count(singular_pat, flags=re.IGNORECASE)
    df[col+'_plural']=df[col].str.count(plural_pat, flags=re.IGNORECASE)
    df[col+'_quotations']=df[col].str.count(quotation_pat, flags=re.IGNORECASE)
    return df


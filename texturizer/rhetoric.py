# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_pattern
 
"""
    texturizer.rhetoric: Feature flags indicating rhetorical devices

"""

########################################################################################

cliches_pat = load_word_pattern('cliches.dat')

jargon_pat = load_word_pattern('jargon.dat')

authority_pat = load_word_pattern('authority.dat')

########################################################################################
def add_text_rhetoric_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the rhetoric trait features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_rhetoric_counts(rez, col)
    return rez

########################################################################################
def add_rhetoric_counts(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the number of pattern matches for feature
    """
    df[col+'_cliches']=df[col].str.count(cliches_pat, flags=re.IGNORECASE)
    df[col+'_jargon']=df[col].str.count(jargon_pat, flags=re.IGNORECASE)
    df[col+'_authority']=df[col].str.count(authority_pat, flags=re.IGNORECASE)
    return df



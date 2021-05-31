# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import statistics
import string
import math
import os
import re

from .process import load_dictionary
from .process import remove_escapes_and_non_printable
from .process import remove_urls_and_tags
 
"""
    texturizer.scarcity: Word Scarcity Statistics

    This module performs word scarcity analysis
"""

########################################################################################

scarcity = load_dictionary('scarcity.dat')

########################################################################################
def add_scarcity_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the scarcity statistics features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_scarcity(rez, col)
    return rez

########################################################################################
def get_scarcity(word):
    if word in scarcity:
        return scarcity[word]
    else:
        return 1.0

########################################################################################
def add_scarcity(df, col):
    """
        Given a pandas dataframe and a column name.
    """
    def cal_features(x, col):
        if x[col]!=x[col]:
            mean_scarcity = 0
            median_scarcity = 0
            max_scarcity = 0
        else:
            text = remove_urls_and_tags( remove_escapes_and_non_printable( x[col] ) ).lower()
            text = text.translate(str.maketrans('', '', string.punctuation)).lower()
            words = text.split()
            scarcities = list(map(get_scarcity, words))
            mean_scarcity = statistics.mean(scarcities)
            median_scarcity = statistics.median(scarcities)
            max_scarcity = max(scarcities)
        return mean_scarcity, median_scarcity, max_scarcity 
    df[ get_scarcity_col_list(col) ] = df.apply(cal_features, col=col, axis=1, result_type="expand") 

    return df

########################################################################################
def get_scarcity_col_list(col):
    return [col+'_scarcity_mean', col+'_scarcity_median', col+'_scarcity_max']



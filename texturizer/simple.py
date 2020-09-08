# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import math
import os

from .process import remove_escapes_and_non_printable
from .process import remove_urls_and_tags
from .process import load_word_list

"""
    texturizer.simple: Basic text feature calculation.

    Calculate statistics such as the average length of words, max word length
    proportion of non stop-words. We also create a clean version of the text
    that can be used by other functions in the library.

    Stop-word list taken from: https://www.textfixer.com/tutorials/common-english-words.txt 

"""

stop_word_list = load_word_list("stop-words.dat") 

########################################################################################
def add_text_summary_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_text_features(rez, col)
    return rez

########################################################################################
def add_text_features(df, col):
    """
        Given a pandas dataframe and a column name.
        calculate the simple text summary features and add them.
    """
    col_len = col + "_len"
    df[col_len] = df[col].apply(null_tolerant_len)
    def cal_features(x, col):
        if x[col]!=x[col]:
            word_count = 0 
            avg_word_len = 0 
            content_wd = 0 
            capital_d = 0
            text = ""
        else:
            text = remove_urls_and_tags( remove_escapes_and_non_printable( x[col] ) )
            chars = null_tolerant_len(x[col])
            capitals = sum(1 for c in x[col] if c.isupper())
            capital_d = capitals/chars
            word_array = x[col].lower().split()
            non_stop_words = list(set(word_array) - set(stop_word_list))
            word_count = len(word_array)
            word_lengths = list(map(len, word_array))
            avg_word_len = sum(word_lengths)/word_count
            content_wd = len(non_stop_words)/len(word_array)
        return word_count, avg_word_len, content_wd, capital_d

    df[ get_simple_col_list(col) ] = df.apply(cal_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def get_simple_col_list(col):
    return [col+'_wc', col+'_avg_wl', col+'_cwd', col+'_caps']

########################################################################################
def null_tolerant_len(x):
    if x != x:
        return 0
    else:
        return len(x)

 
########################################################################################

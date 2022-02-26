# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_pattern
 
"""
    texturizer.reason: Reason and Argument feature flags

    Some ideas taken from these articles
    Logical Reasoning: Bradley H. Dowden
    https://www.flexiblemindtherapy.com/uploads/6/5/5/2/65520823/logical-reasoning.pdf
"""

########################################################################################

premises_pat = load_word_pattern('premises.dat')
premises_re = re.compile(premises_pat)

reasoning_pat = load_word_pattern('reasoning.dat')
reasoning_re = re.compile(reasoning_pat)

conclusions_pat = load_word_pattern('conclusions.dat')
conclusions_re = re.compile(conclusions_pat)


########################################################################################
def add_text_reason_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the reasoning features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_reason_counts(rez, col)
    return rez

########################################################################################
def add_reason_counts(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the number of keyword matches for each trait
    """
    df[col+'_premise']=df[col].str.count(premises_pat, flags=re.IGNORECASE)
    df[col+'_reason']=df[col].str.count(reasoning_pat, flags=re.IGNORECASE)
    df[col+'_conclusion']=df[col].str.count(conclusions_pat, flags=re.IGNORECASE)
    return df


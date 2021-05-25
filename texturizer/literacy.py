# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list
from .process import load_word_pattern

"""
    texturizer.literacy: Literacy feature flags

    Simple word matching to generate features for common literacy problems.
    This includes typos or spelling mistakes and some simple grammar problems,
    for example, not capitalizing the first word of a sentence.

"""

########################################################################################
misspelling_pat = load_word_pattern('misspelling.dat')
misspelling_re = re.compile(misspelling_pat)
 
grammar_pat = "[ '(\"][aA] [AaEeIiOoUu]|[^.][^A-Z]\. [a-z]|\b(\w+)\b \b\1\b"
grammar_re = re.compile(grammar_pat)

########################################################################################
def add_text_literacy_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple literacy features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_literacy_features(rez, col)
    return rez

########################################################################################
def add_literacy_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for literacy.
    """

    def lit_features(x, col):
        misspelling = 0
        grammar_err = 0
        if x[col]!=x[col]:
            misspelling = 0
        else:
            text = (x[col])
            grammar_err = len(grammar_re.findall(text))
            text = (x[col].lower())
            misspelling = len(misspelling_re.findall(text))
        return misspelling, grammar_err

    df[[ col+'_misspelling', col+'_grammar_err' ]] = df.apply(lit_features, col=col, axis=1, result_type="expand")

    return df
 

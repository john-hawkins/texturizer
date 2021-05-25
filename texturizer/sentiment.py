# -*- coding: utf-8 -*-
from textblob import TextBlob
import numpy as np 
import re

from .process import load_word_pattern

"""
    texturizer.sentiment: Sentiment feature flags

    We use multiple sets of words lists for different sentiment features


    Hu and Liu

    This is a large list of postive and negative words. Taken from:
    http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

    Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
       Proceedings of the ACM SIGKDD International Conference on Knowledge
       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
       Washington, USA,

    AFINN

    Smaller list created by extracting extreme sentiment words from the AFINN
    lists. Extracted from:
    http://www2.imm.dtu.dk/pubdb/pubs/6010-full.html 

    This derived database of words is copyright protected and distributed under
    "Open Database License (ODbL) v1.0"
    http://www.opendatacommons.org/licenses/odbl/1.0/ 


    TODO

    Investgate how to use (license and processing requirements).

    http://www.wjh.harvard.edu/~inquirer/homecat.htm
"""

########################################################################################

positive_pat_large = load_word_pattern('positive-words.dat')
negative_pat_large = load_word_pattern('negative-words.dat')

positive_pat = load_word_pattern('positive.dat')
negative_pat = load_word_pattern('negative.dat')

########################################################################################
def add_text_sentiment_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the sentiment features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_sentiment_features(rez, col)
        rez = add_textblob_features(rez, col)
    return rez

########################################################################################
def add_textblob_features(df, col):
    def tb_features(x, col):
        if x[col]!=x[col]:
            subjectivity = 0.0 #np.nan
            polarity = 0.0     #np.nan
        else:
            text = ( x[col] )
            blob = TextBlob(text)
            subjectivity = blob.sentiment.subjectivity
            polarity = blob.sentiment.polarity
        return polarity, subjectivity

    df[[ col+'_tb_polarity', col+'_tb_subjectivity' ]] = df.apply(tb_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def add_sentiment_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match features for sentiment.
    """
    wc_col = col+'_wc' # This is ALWAYS computed first
    df[col+'_positive']  = df[col].str.count(positive_pat, flags=re.IGNORECASE).fillna(0)
    df[col+'_negative']  = df[col].str.count(negative_pat, flags=re.IGNORECASE).fillna(0)
    df[col+'_sentiment'] = (df[col+'_positive'] - df[col+'_negative'] )/df[wc_col]

    return df 


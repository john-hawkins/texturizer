import sys
import numpy as np
import jellyfish
import textdistance
import pandas as pd

#################################################################################
def add_comparison_features(df,columns):
    """
        This is the entry point to add all the core text similarity features.
        Note: We left out Ratcliff Obershelp from the set of metrics because it
        takes close to an order of magnitude longer to compute.

        Initial version just includes 4 string edit distance metrics. 
    """
    return add_string_match_features(df,columns)

#################################################################################
def add_string_match_features(df,columns):
    """
    Return a copy of a dataframe with features describing matching
    between the set of named text columns
    """
    def sm_features(x, col1, col2):
        if (x[col1] != x[col1]) or (x[col2] != x[col2]):
            jd = np.nan
            ld = np.nan
            ji = np.nan
            sd = np.nan
        else:
            raw_text1 = x[col1].lower()
            raw_text2 = x[col2].lower()
            jd = jellyfish.jaro_distance(raw_text1,raw_text2)
            ld = jellyfish.levenshtein_distance(raw_text1,raw_text2)
            ji = textdistance.jaccard(raw_text1,raw_text2)
            sd = textdistance.sorensen(raw_text1,raw_text2 )
        return jd, ld, ji, sd

    col_number = len(columns)
    for i in range( col_number-1 ):
        for j in range(i+1,col_number):
            col1 = columns[i]
            col2 = columns[j]
            prefix = col1 + "_vs_" + col2
            df[[prefix+'_jd', prefix+'_ld',prefix+'_ji',prefix+'_sd']] = df.apply(sm_features, col1=col1,col2=col2, axis=1, result_type="expand")
    return df


#################################################################################
def add_ratcliff_obershelp(df,columns):
    """
    Return a copy of a dataframe with features describing matching
    between the set of named text columns
    """
    def sm_features(x, col1, col2):
        if (x[col1] != x[col1]) or (x[col2] != x[col2]):
            ro = np.nan
        else:
            raw_text1 = x[col1].lower()
            raw_text2 = x[col2].lower()
            ro = textdistance.ratcliff_obershelp(raw_text1,raw_text2)
        return ro

    col_number = len(columns)
    for i in range( col_number-1 ):
        for j in range(i+1,col_number):
            col1 = columns[i]
            col2 = columns[j]
            prefix = col1 + "_vs_" + col2
            df[[prefix+'_rat_obers']] = df.apply(sm_features, col1=col1,col2=col2, axis=1, result_type="expand")
    return df




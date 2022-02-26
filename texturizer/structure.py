# -*- coding: utf-8 -*-

import spacy
from .process import eprint

try:
   nlp = spacy.load("en_core_web_sm")
except:
   eprint(" * WARNING: Structure features require the SpaCY language model : en_core_web_sm")

"""
    texturizer.structure - Text Structure Features

    Using SpacY to parse a block of text we then transform the text into a structural
    representation and convert it into features.

"""

########################################################################################
def add_text_structure_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the structure of the text.
    """
    rez = df.copy()
    for col in columns:
        rez = add_structure_representation(rez, col)
    return rez

########################################################################################
def add_structure_representation(df, col):
    """
        Given a pandas dataframe and a column name
        add a column with the text represented as a string of structural features.
    """

    def structure_features(x, col):
        if x[col]!=x[col]:
            rez = ""
        else:
            text = (x[col])
            doc = nlp(text)
            index = 0
            rez = ""
            for token in doc:
               if index > 0:
                   rez = rez + " "
               if token.is_punct:
                   rez = rez + token
               else:
                   rez = rez + token.tag_
               index = index + 1
        return rez 

    df[[ col+'_structure' ]] = df.apply(structure_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################






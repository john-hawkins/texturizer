# -*- coding: utf-8 -*-
import numpy as np
import spacy
from .process import eprint

# THIS IS THE SIZE OF THE SPACY VECTOR FROM: en_core_web_sm
EMBEDDING_DIM = 96

try:
   nlp = spacy.load("en_core_web_sm")
except:
   eprint(" * WARNING: POS features require the SpaCY language model : en_core_web_sm")

"""
    texturizer.embedding Text Embedding using spaCy

    We use the spacy word vector representations to create an aggregate of the text block.

    Notes: I have implemented this inside a single 'apply' function which gives 
    some speed advantage. However, it is still slow. I am still looking for ways
    to speed this up.
"""

########################################################################################
def add_text_embedding_features(df, columns, type="sum"):
    """
        Given a pandas dataframe and a set of column names.
        calculate the embedding features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_embedding_features(rez, col, type)
    return rez

########################################################################################
def add_embedding_features(df, col, type):
    """
        Given a pandas dataframe and a column name.
        add features that embed the text content into a semantic space.
    """

    def vec_feats(x, col):
        if x[col]!=x[col]:
            vec = np.zeros(EMBEDDING_DIM)
        else:
            text = (x[col])
            doc = nlp(text)
            index = 0
            vec = np.zeros(EMBEDDING_DIM)
            for token in doc:
               vec = vec + token.vector
               index = index + 1
            if type=='normalize':
               vec = vec / index
        return vec.tolist() 

    df[ get_vec_column_names(col) ] = df.apply(vec_feats, col=col, axis=1, result_type="expand")

    return df
 
########################################################################################
def get_vec_column_names(col):
    return [ col + "_vec_" + str(i) for i in range(0,EMBEDDING_DIM)]



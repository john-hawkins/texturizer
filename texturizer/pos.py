# -*- coding: utf-8 -*-

import spacy
from .process import eprint

try:
   nlp = spacy.load("en_core_web_sm")
except:
   eprint(" * WARNING: POS features require the SpaCY language model : en_core_web_sm")

"""
    texturizer.pos Part of Speech features using spaCy

    Extraction of part of speech tags for a block of text and then generation
    of numerical features that summarise the grammatical structure of that text.

    Notes: I have implemented this inside a single 'apply' function which gives 
    some speed advantage. However, it is still slow. I am still looking for ways
    to speed this up.
"""

########################################################################################
def add_text_pos_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        calculate the part of speech features and add them.
    """
    rez = df.copy()
    for col in columns:
        rez = add_pos_features(rez, col)
    return rez

########################################################################################
def add_pos_features(df, col):
    """
        Given a pandas dataframe and a column name.
        add features for the proportion of dominant parts of speech
        Nouns, Verbs, Adjectives, Adverbs, Pronouns and Adpositions
    """

    def pos_features(x, col):
        nouns = 0
        verbs = 0
        adj = 0
        adv = 0
        pron = 0
        adp = 0
        index = 1
        if x[col]!=x[col]:
            nouns = 0
        else:
            text = (x[col])
            doc = nlp(text)
            index = 0
            for token in doc:
               if token.pos_ == "VERB":
                   verbs = verbs + 1
               if token.pos_ == "NOUN":
                   nouns = nouns + 1
               if token.pos_ == "ADJ":
                   adj = adj + 1
               if token.pos_ == "ADV":
                   adv = adv + 1
               if token.pos_ == "PRON":
                   pron = pron + 1
               if token.pos_ == "ADP":
                   adp = adp + 1
               index = index + 1
        return nouns/index, verbs/index, adj/index, adv/index, pron/index, adp/index

    df[[ col+'_nouns', col+'_verbs', col+'_adj', col+'_adv', col+'_pron', col+'_adp' ]] = df.apply(pos_features, col=col, axis=1, result_type="expand")

    return df
 

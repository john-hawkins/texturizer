# -*- coding: utf-8 -*-
import pandas as pd 
import numpy as np
import codecs
import re

from .process import load_word_list
from .process import load_word_pattern
from .process import remove_urls_and_tags
from .process import remove_escapes_and_non_printable

smiles = load_word_list("emoticons-smile.dat")
laughs = load_word_list("emoticons-laugh.dat")
winks = load_word_list("emoticons-wink.dat")
cheekys = load_word_list("emoticons-wink.dat")
kisses = load_word_list("emoticons-kiss.dat")
happycrys = load_word_list("emoticons-happy-cry.dat")
crys = load_word_list("emoticons-cry.dat")
sads = load_word_list("emoticons-sad.dat")
shocks = load_word_list("emoticons-shock.dat")
sceptics = load_word_list("emoticons-sceptical.dat")
 
fwd_regex = "[:;8BX]['’`]{0,1}[-=^oc]{0,2}[DPO0J3ox,Þþb@*\\|/()<>{}\[\]]{1,2}"
fwd_re = re.compile(fwd_regex)
bck_regex = "[@*\\|/()<>{}\[\]]{1,2}[-=^]{0,2}['’`]{0,1}[:;]"
bck_re = re.compile(bck_regex)

 
"""
    texturizer.emoticons: Emoticon Recognition Text Features
 
    The functions in this library will add columns to a dataframe that indivate
    whether there are emoticons in certain columns of text, and whether those
    emoticons represent one of the more common emotions.

    NOTE: In developing these regexes I have deliberately ignored certain emoticons 
     because of the likelihood of false positive matches in text containing brackets
     For example emoticons: 8) or (B will not be matched.

    To avoid matching characters inside document markup language tags there is a 
    rudimentary regex based tag removal and unescaped version of the text that is
    expecte to have been generated in the intial simple text function run by the program. 
    This will remove URLS and HTML tags before trying to match emoticons.

    Some references used when considering which empticons to include:

    https://www.unglobalpulse.org/2014/10/emoticon-use-in-arabic-spanish-and-english-tweets/

    https://www.researchgate.net/publication/266269913_From_Emoticon_to_Universal_Symbolic_Signs_Can_Written_Language_Survive_in_Cyberspace

    https://www.sciencedirect.com/science/article/abs/pii/S0950329317300939

    https://www.semanticscholar.org/paper/An-Approach-towards-Text-to-Emoticon-Conversion-and-Jha/3b81505fa7fec81563b2dafae3939fa1b07f3a98

    https://www.qualitative-research.net/index.php/fqs/article/view/175/391

    https://www.researchgate.net/publication/221622114_M_Textual_Affect_Sensing_for_Sociable_and_Expressive_Online_Communication

"""


########################################################################################
def add_text_emoticon_features(df, columns):
    """
        Given a pandas dataframe and a set of column names.
        Add features that detect the presence of emoticons.
    """
    rez = df.copy()
    for col in columns:
        rez = add_emoticon_features(rez, col)
    return rez


########################################################################################
def add_emoticon_features(df, col):
    """
        Given a pandas dataframe and a column name.
        Check for emoticons in the column and add a set of features
        that indicate both the presence and emotional flavour of the emoticon.
    """
    def cal_features(x, col):
        emos = 0 
        smiley = 0 
        wink = 0 
        kiss = 0
        happycry = 0
        laugh = 0
        cheeky = 0
        crying = 0
        sad = 0
        shock = 0 
        sceptic = 0 
        if x[col]==x[col]:
            text = remove_urls_and_tags( remove_escapes_and_non_printable( x[col] ) )
            matches = fwd_re.findall(text)
            bck_matches = bck_re.findall(text)
            if len(matches)>0 or len(bck_matches)>0:
                matches.extend(bck_matches)
                emos = len(matches)
                if set(matches).intersection( smiles ):                
                    smiley = 1
                if set(matches).intersection( crys ):        
                    crying = 1
                if set(matches).intersection( winks ):                
                    wink = 1
                if set(matches).intersection( kisses ):                
                    kiss = 1
                if set(matches).intersection( sads ):                
                    sad = 1
                if set(matches).intersection( shocks ):                
                    shock = 1
                if set(matches).intersection( sceptics ):                
                    sceptic = 1
                if set(matches).intersection( laughs ):                
                    laugh = 1
                if set(matches).intersection( cheekys ):                
                    cheeky = 1
                if set(matches).intersection( happycrys ):                
                    happycry = 1
        pos = smiley + wink + kiss + happycry + laugh + cheeky
        neg = crying + sad + shock + sceptic
        sent = pos - neg
        return emos,smiley,wink,kiss,happycry,laugh,cheeky,crying,sad,shock,sceptic,pos,neg,sent
 
    df[ get_emoticon_col_list(col) ] = df.apply(cal_features, col=col, axis=1, result_type="expand")

    return df

########################################################################################
def get_emoticon_col_list(col):
    return [col+'_emoticons', col+'_emo_smiley', col+'_emo_wink', col+'_emo_kiss', col+'_emo_happycry', col+'_emo_laugh', col+'_emo_cheeky', col+'_emo_cry', col+'_emo_sad', col+'_emo_shock', col+'_emo_sceptic', col+'_emo_pos', col+'_emo_neg', col+'_emo_sentiment'] 



# -*- coding: utf-8 -*-
import functools
import pandas as pd 
import numpy as np

from .process import start_profile
from .process import end_profile
from .simple import add_text_summary_features
from .pos import add_text_pos_features
from .topics import add_text_topics_features
from .profanity import add_text_profanity_features
from .traits import add_text_trait_features
from .rhetoric import add_text_rhetoric_features
from .sentiment import add_text_sentiment_features
from .literacy import add_text_literacy_features
from .emoticons import add_text_emoticon_features
from .comparison import add_comparison_features
from .scarcity import add_scarcity_features
from .embedding import add_text_embedding_features

"""
    texturizer.featurize: Core functions to apply a set of features to a data frame.
"""
########################################################################################

def process_df(df, params):
    """ 
    process_df: Function that co-ordinates the process of generating the features
    
    """ 
    start_profile("simple")
    simple = add_text_summary_features( df, params["columns"] )
    end_profile("simple")
    if params["comparison"] :
        start_profile("comparison")
        simple = add_comparison_features( simple, params["columns"] )
        end_profile("comparison")
    if params["profanity"] :
        start_profile("profanity")
        simple = add_text_profanity_features( simple, params["columns"] )
        end_profile("profanity")
    if params["sentiment"] :
        start_profile("sentiment")
        simple = add_text_sentiment_features( simple, params["columns"] )
        end_profile("sentiment")
    if params["scarcity"] :
        start_profile("scarcity")
        simple = add_scarcity_features( simple, params["columns"] )
        end_profile("scarcity")
    if params["emoticons"] :
        start_profile("emoticons")
        simple = add_text_emoticon_features( simple, params["columns"] )
        end_profile("emoticons")
    if params["embedding"] :
        start_profile("embedding")
        simple = add_text_embedding_features( simple, params["columns"] )
        end_profile("embedding")
    if params["topics"] :
        start_profile("topics")
        if params["count_matches"] :
            simple = add_text_topics_features( simple, params["columns"], 'count' )
        else:
            simple = add_text_topics_features( simple, params["columns"] )
        end_profile("topics")
    if params["traits"] :
        start_profile("traits")
        simple = add_text_trait_features( simple, params["columns"] )
        end_profile("traits")
    if params["rhetoric"] :
        start_profile("rhetoric")
        simple = add_text_rhetoric_features( simple, params["columns"] )
        end_profile("rhetoric")
    if params["pos"] :
        start_profile("pos")
        simple = add_text_pos_features( simple, params["columns"] )
        end_profile("pos")
    if params["literacy"] :
        start_profile("literacy")
        simple = add_text_literacy_features( simple, params["columns"] )
        end_profile("literacy")
    return simple

########################################################################################

def generate_feature_function(parameters):
    """
        This function will take the processed command line arguments that determine
        the feature to apply and partially apply them to the process_df function.
        Returning a function that can be used to apply those parameters to multiple
        chunks of a dataframe.
    """
    return functools.partial(process_df, params = parameters)


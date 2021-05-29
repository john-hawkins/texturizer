from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import numpy as np
import re

from .featurize import generate_feature_function

class TextTransform(TransformerMixin, BaseEstimator):
    """
        This class implements a SciKit Learn compatible Transformer for
         convert a text column into a series of numeric values.
         You specify the transformations you want as an array of named
         feature groups.

        columns: Array(String) Names of the text columns to process.
        transforms: Array(String) Names of the feature sets to generate
                     Options: profanity, topics, pos, rhetoric, literacy, traits
    """

    def __init__(self, columns, transforms=['simple']):
        self.transforms = transforms
        self.columns = columns
        self.config = self.generate_feature_config(columns, transforms)
        self.func = generate_feature_function(self.config)
        

    def fit(self, X, y=None, **fit_params):
        return self
    
    def transform(self, X, y=None, **transform_params):
        """
            Transform the matrix of values
             -- need to deal with single or multiple columns
        """
        rez = self.func(X)        

        # Might need this later 
        #if X.__class__.__name__ == "DataFrame":
        #    X = X.values

        # REMOVE THE TEXT COLUMNS -- PARAMETERIZE THIS LATER
        for col in self.columns:
            rez.drop(col, inplace=True, axis=1)

        return rez 


    #############################################################
    def generate_feature_config(self, columns, params):
        """
        We need to process the params into a particular data structure 
        for the dataframe processing function to recognize. 
        """
        result = {
              "columns":columns,
              "profanity":False,
              "sentiment":False,
              "emoticons":False,
              "topics":False,
              "count_matches":False,
              "traits":False,
              "rhetoric":False,
              "pos":False,
              "literacy":False,
              "scarcity":False,
              "comparison":False,
              "embedding":False
        }
        if "profanity" in params:
           result["profanity"]=True
        if "sentiment" in params:
           result["sentiment"]=True
        if "scarcity" in params:
           result["scarcity"]=True
        if "emoticons" in params:
           result["emoticons"]=True
        if "topics" in params:
           result["topics"]=True
        if "count_matches" in params:
           result["count_matches"]=True
        if "pos" in params:
           result["pos"]=True
        if "traits" in params:
           result["traits"]=True
        if "rhetoric" in params:
           result["rhetoric"]=True
        if "literacy" in params:
           result["literacy"]=True
        if "comparison" in params:
           result["comparison"]=True
        if "embedding" in params:
           result["embedding"]=True

        return result



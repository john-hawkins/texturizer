# -*- coding: utf-8 -*-
 
""" texturizer.texturizer: provides entry point main()."""
 
__version__ = "0.1.0"
from io import StringIO
import numpy as np
import pandas as pd
import sys
import os

from .process import load_complete_dataframe
from .process import initialise_profile
from .process import start_profile
from .process import end_profile
from .process import print_profiles
from .simple import add_text_summary_features
from .pos import add_text_pos_features
from .topics import add_text_topics_features
from .profanity import add_text_profanity_features
from .personality import add_text_personality_features
from .sentiment import add_text_sentiment_features
from .literacy import add_text_literacy_features
from .emoticons import add_text_emoticon_features
from .comparison import add_comparison_features
from .config import max_filesize
 
def main():
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        params = get_cmd_line_params(sys.argv)
        #print(params)

        if not os.path.exists(params["dataset"]):
            print("ERROR: Dataset does not exist")
            print_usage(sys.argv)
            exit(1)
        filesize = os.stat(params["dataset"]).st_size
        if filesize<max_filesize:
            df = load_complete_dataframe( params["dataset"] )
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
            if params["emoticons"] :
                start_profile("emoticons")
                simple = add_text_emoticon_features( simple, params["columns"] )
                end_profile("emoticons")
            if params["topics"] :
                start_profile("topics")
                if params["count_matches"] :
                    simple = add_text_topics_features( simple, params["columns"], 'count' )
                else:
                    simple = add_text_topics_features( simple, params["columns"] )
                end_profile("topics")
            if params["traits"] :
                start_profile("traits")
                simple = add_text_personality_features( simple, params["columns"] )
                end_profile("traits")
            if params["pos"] :
                start_profile("pos")
                simple = add_text_pos_features( simple, params["columns"] )
                end_profile("pos")
            if params["literacy"] :
                start_profile("literacy")
                simple = add_text_literacy_features( simple, params["columns"] )
                end_profile("literacy")
            print_output( simple )
        else:
            print("Oversize data - This functionality is not yet built")

        print_profiles()

#############################################################
def print_output(df):
    output = StringIO()
    df.to_csv(output,index=False)
    print(output.getvalue())
 
#############################################################
def get_cmd_line_params(argv):
    """ parse out the option from an array of command line arguments """
    data = argv[-1]
    options = argv[1:-1]
    result = {"dataset":data,
              "columns":[], 
              "profanity":False, 
              "sentiment":False, 
              "emoticons":False, 
              "topics":False, 
              "count_matches":False, 
              "traits":False, 
              "pos":False, 
              "literacy":False, 
              "comparison":False, 
              "embedding":False
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-literacy":
            result["literacy"]=True
        if parts[0] == "-profanity":
            result["profanity"]=True
        if parts[0] == "-sentiment":
            result["sentiment"]=True
        if parts[0] == "-topics":
            result["topics"]=True
            if len(parts)>1:
                if parts[1] == 'count':
                    result["count_matches"]=True
        if parts[0] == "-traits":
            result["traits"]=True
        if parts[0] == "-pos":
            result["pos"]=True
        if parts[0] == "-emoticons":
            result["emoticons"]=True
        if parts[0] == "-embedding":
            result["embedding"]=True
        if parts[0] == "-comparison":
            result["comparison"]=True
        if parts[0] == "-columns":
            cols = parts[1].split(",")
            result["columns"]=cols

    return result

#############################################################
def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " [ARGS] <PATH TO DATASET>")
    print("  <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf")
    print(" [ARGS] In most cases these are switches that turn on the feature type")
    print("  -columns=<COMMA SEPARATED LIST>. Default: apply to all string columns.")
    print("  -topics OR -topics=count. Default: False. Match words from common topics (or count matches).")
    print("  -traits Default: False. Word usage for personality traits.")
    print("  -pos Default: False. Part of speech proportions.")
    print("  -literacy Default: False. Checks for common literacy markers.")
    print("  -profanity Default: False. Profanity check flags.")
    print("  -sentiment Default: False. Words counts for positive and negative sentiment.")
    print("  -emoticons Default: False. Emoticon check flags.")
    print("  -comparison Default: False. Cross-column comparisons.")
    print("")



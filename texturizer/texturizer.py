# -*- coding: utf-8 -*-
 
""" texturizer.texturizer: provides entry point main()."""
 
import pandas as pd
import sys
import os

from .process import load_complete_dataframe
from .process import process_file_in_chunks
from .process import initialise_profile
from .process import print_profiles
from .process import print_output

from .featurize import generate_feature_function

from .config import max_filesize
 
def main():
    """Main texturizer application entry point.
       parses out CL options and determine the size of the file.
       Then process the file for the requested features
    """
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        params = get_cmd_line_params(sys.argv)

        if not os.path.exists(params["dataset"]):
            print("ERROR: Dataset does not exist")
            print_usage(sys.argv)
            exit(1)

        initialise_profile()
        feature_func = generate_feature_function(params)

        filesize = os.stat(params["dataset"]).st_size
        if filesize<max_filesize:
            df = load_complete_dataframe( params["dataset"] )
            simple = feature_func(df)
            print_output( simple )
        else:
            process_file_in_chunks(params["dataset"], feature_func)

        print_profiles()


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
              "rhetoric":False, 
              "pos":False, 
              "literacy":False, 
              "scarcity":False, 
              "comparison":False, 
              "embedding":False
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-literacy":
            result["literacy"]=True
        if parts[0] == "-profanity":
            result["profanity"]=True
        if parts[0] == "-scarcity":
            result["scarcity"]=True
        if parts[0] == "-sentiment":
            result["sentiment"]=True
        if parts[0] == "-topics":
            result["topics"]=True
            if len(parts)>1:
                if parts[1] == 'count':
                    result["count_matches"]=True
        if parts[0] == "-traits":
            result["traits"]=True
        if parts[0] == "-rhetoric":
            result["rhetoric"]=True
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
    print("  -columns=<COMMA SEPARATED LIST>. REQUIRED")
    print("  -topics OR -topics=count. Default: False. Match words from common topics (or count matches).")
    print("  -traits Default: False. Word usage for personality traits.")
    print("  -rhetoric Default: False. Word usage for rhetorical devices.")
    print("  -pos Default: False. Part of speech proportions.")
    print("  -literacy Default: False. Checks for common literacy markers.")
    print("  -profanity Default: False. Profanity check flags.")
    print("  -sentiment Default: False. Words counts for positive and negative sentiment.")
    print("  -scarcity Default: False. Word scarcity scores.")
    print("  -emoticons Default: False. Emoticon check flags.")
    print("  -embedding Default: False. Normalised Aggregate of Word Embedding Vectors.")
    print("  -comparison Default: False. Cross-column comparisons.")
    print("")



# -*- coding: utf-8 -*-
 
""" texturizer.texturizer: provides entry point main()."""
 
__version__ = "0.1.0"
from io import StringIO
import numpy as np
import pandas as pd
import sys
import os

from .process import load_complete_dataframe
from .simple import add_text_summary_features
from .pos import add_text_pos_features
from .topics import add_text_topics_features
from .profanity import add_text_profanity_features
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
            simple = add_text_summary_features( df, params["columns"] )
            if params["comparison"] :
                simple = add_comparison_features( simple, params["columns"] )
            if params["profanity"] :
                simple = add_text_profanity_features( simple, params["columns"] )
            if params["emoticons"] :
                simple = add_text_emoticon_features( simple, params["columns"] )
            if params["topics"] :
                simple = add_text_topics_features( simple, params["columns"] )
            if params["pos"] :
                simple = add_text_pos_features( simple, params["columns"] )
            if params["literacy"] :
                simple = add_text_literacy_features( simple, params["columns"] )
            print_output( simple )
        else:
            print("Oversize data - This functionality is not yet built")


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
              "emoticons":False, 
              "topics":False, 
              "pos":False, 
              "literacy":False, 
              "comparison":False, 
              "embedding":False
    }
    for o in options:
        parts = o.split("=")
        if parts[0] == "-literacy":
            if parts[1] == 'True':
                result["literacy"]=True
        if parts[0] == "-profanity":
            if parts[1] == 'True':
                result["profanity"]=True
        if parts[0] == "-topics":
            if parts[1] == 'True':
                result["topics"]=True
        if parts[0] == "-pos":
            if parts[1] == 'True':
                result["pos"]=True
        if parts[0] == "-emoticons":
            if parts[1] == 'True':
                result["emoticons"]=True
        if parts[0] == "-embedding":
            if parts[1] == 'True':
                result["embedding"]=True
        if parts[0] == "-comparison":
            if parts[1] == 'True':
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
    print(" [ARGS] ")
    print("  -columns=<COMMA SEPARATED LIST>. Default: apply to all string columns.")
    print("  -topics=<True or False>. Default: False. Counts of words from common topics.")
    print("  -pos=<True or False>. Default: False. Part of speech proportions.")
    print("  -literacy=<True or False>. Default: False. Checks for common literacy markers.")
    print("  -profanity=<True or False>. Default: False. Profanity check flags.")
    print("  -emoticons=<True or False>. Default: False. Emoticon check flags.")
    print("  -comparison=<True or False>. Default: False. Cross-column comparisons.")
    print("")



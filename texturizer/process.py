# -*- coding: utf-8 -*-
from __future__ import print_function
from io import StringIO
import datetime as dt
import pkg_resources
import pandas as pd 
import numpy as np
import json
import codecs
import sys
import os
import re

from .config import max_filesize

"""
    texturizer.process: Support functions for the texturizer package.
                        Including functions for loading word lists, logging processing times,
                        and iteratively processing a large dataset in chunks.
"""
########################################################################################
resource_package = __name__

def load_dictionary(filename, escape=False):
    """
    Utility function to load a json serialised dictionary
    """
    _path = '/'.join(('data', filename))
    rawd = pkg_resources.resource_string(resource_package, _path).decode("utf-8")
    if escape:
        rawd = re.escape(rawd)
    return json.loads(str(rawd)) 

########################################################################################
def load_word_list(filename, escape=False):
    """
    Utility function to load topic vocab word lists for pattern matching.
    """
    _path = '/'.join(('data', filename))
    rawd = pkg_resources.resource_string(resource_package, _path).decode("utf-8")
    rawd = rawd[:-1]
    if escape:
        rawd = re.escape(rawd)
    word_list = str(rawd).split("\n")
    _list = [i for i in word_list if i]
    return _list

########################################################################################

def load_word_pattern(filename, prefix="", pluralize=True, bound=True, escape=False):
    word_list = load_word_list(filename, escape=escape)
    if bound:
       delimiter = "\\b"
    else:
       delimiter = ""
    pattern_start = prefix + delimiter
    if pluralize:
        tail = "s*" + delimiter
        joiner = "s*" + delimiter + "|" + delimiter
    else:
        tail = delimiter
        joiner = delimiter + "|" + delimiter

    pattern = pattern_start  + ( joiner.join(word_list) ) + tail
    return pattern

########################################################################################
"""
   This is a set of functions to allow the application to print time
   profiles of the various feature engines to STDERR.
"""

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

profiles = {}

def initialise_profile():
    profiles = {}

def start_profile(proc_name):
    n1=dt.datetime.now()
    if proc_name in profiles:
        profiles[proc_name]["start"] = n1
    else:
        profiles[proc_name] = {"start":n1}

def end_profile(proc_name):
    n2 = dt.datetime.now()
    n1 = profiles[proc_name]["start"]
    total = n2-n1
    profiles[proc_name]["end"] = n2
    if "total" in profiles[proc_name]:
        curr_total = profiles[proc_name]["total"]
        profiles[proc_name]["total"] = curr_total + total
    else:
        profiles[proc_name]["total"] = total

def print_profiles():
    eprint("Computation Time Profile for each Feature Set")
    eprint("---------------------------------------------")
    for k in profiles.keys():
        eprint(padded(k), str(profiles[k]["total"]) ) 

def padded(k, padto=20):
    spacer_len = padto - len(k)
    return k + (" "*spacer_len)

########################################################################################
def process_file_in_chunks(path_to_file, function_to_apply):
    """
        Given a path to a large dataset we will iteratively load it in chunks and 
        apply the supplied function to and write the result to the output stream.
    """
    fsize = os.stat(path_to_file).st_size
    sample_prop = max_filesize / fsize 
    line_count = count_lines(path_to_file)
    chunks = round(line_count * sample_prop)
    data_iterator = pd.read_csv(path_to_file, chunksize=chunks, low_memory=False)
    total_chunks = 0
    for index, chunk in enumerate(data_iterator, start=0):
        startpoint = 0 + (index*chunks)
        total_chunks = index + 1
        temp = function_to_apply(chunk)
        if total_chunks==1:
            print_output(temp, header=True)
        else:
            print_output(temp, header=False)
    
    eprint("Chunks processed: ", total_chunks)
 
########################################################################################
def print_output(df, header=True):
    output = StringIO()
    df.to_csv(output,index=False, header=header)
    print(output.getvalue(), end = '')

########################################################################################
def extract_file_extension(path_to_file):
    return os.path.splitext(path_to_file)[1]

########################################################################################
def load_complete_dataframe(path_to_file):
    """
        We load the entire dataset into memory, using the file extension to determine
        the expected format. We are using encoding='latin1' because it appears to 
        permit loading of the largest variety of files.
        Representation of strings may not be perfect, but is not important for generating a
        summarization of the entire dataset.
    """
    extension = extract_file_extension(path_to_file).lower()
    if extension == ".csv":
        df = pd.read_csv(path_to_file, encoding='latin1', low_memory=False)
        return df
    if extension == ".tsv":
        df = pd.read_csv(path_to_file, encoding='latin1', sep='\t', low_memory=False)
        return df
    if extension == ".xls" or extension == ".xlsx" or extension == ".odf" :
        df = pd.read_excel(path_to_file)
        return df

    raise ValueError("Unsupported File Type")

########################################################################################
def count_lines(path_to_file):
    """
    Return a count of total lines in a file. In a way that filesize is irrelevant
    """
    count = 0
    for line in open(path_to_file): count += 1
    return count

########################################################################################
def len_or_null(val):
    """ 
       Alternative len function that will simply return numpy.NA 
       for invalid values. This is needed to get sensible results 
       when running len over a column that may contain nulls
    """
    try:
        return len(val)
    except:
        return np.nan

########################################################################################
def isNaN(num):
    return num != num

########################################################################################
def remove_urls_and_tags(text):
    """
        Remove any obvious text elements that appear to be either 
        URLs or HTML tags
    """
    patterns = ["https?://[-._a-z0-9A-Z]*","</?[a-zA-Z]* ?[a-zA-Z'=.]* ?/?>","\\[tnrf]"]
    new_text = text
    for p in patterns:
        new_text = re.sub(p, ' ', new_text)
    return new_text

def remove_urls(text):
    pattern = "https?://[-._a-z0-9A-Z]*"
    new_text = re.sub(pattern, ' ', text)
    return new_text

def remove_tags(text):
    pattern = "</?[a-zA-Z]* ?[a-zA-Z'=.]* ?/?>"
    new_text = re.sub(pattern, ' ', text)
    return new_text

########################################################################################
def remove_escapes_and_non_printable(text):
    """
        Apply the codecs escape to decode any escaped characters.
        Then apply a regex to remove any non printable characters
    """
    try:
        new_text0 = codecs.escape_decode(text)[0].decode("utf-8")
    except:
        new_text0 = text
    pattern = "\0|\n|\r|\b|\t|\f|\v"
    new_text1 = re.sub(pattern, " ", new_text0)
    return new_text1

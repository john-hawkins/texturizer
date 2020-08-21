# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os

from .config import max_filesize
 
"""
    texturizer.process: Functions for iteratively processing a large dataset
                        in chunks to add the features.

    The goal of this module is to permit the feature generation to be done
    on files larger than the memory by processing in chunks.
"""
########################################################################################
resource_package = __name__

def load_word_list(filename):
    """
    Utility function to load topic vocab word lists for pattern matching.
    """
    _path = '/'.join(('data', filename))
    rawd = pkg_resources.resource_string(resource_package, _path)
    word_list = str(rawd).split('\n')
    _list = [i for i in word_list if i]
    return _list

########################################################################################
def process_file_in_chunks(path_to_file, function_to_apply, output_stream):
    """
        Given a path to a large dataset we will iteratively load it in chunks and 
        apply the supplied function to and write the result to the output stream.
    """
    fsize = os.stat(path_to_file).st_size
    sample_prop = max_filesize / fsize 
    line_count = count_lines(path_to_file)
    chunks = round(line_count * sample_prop)
    temp = pd.DataFrame()
    data_iterator = pd.read_csv(path_to_file, chunksize=chunks, low_memory=False)
    total_chunks = 0
    stream = start_stream(output_stream)
    for index, chunk in enumerate(data_iterator, start=0):
        startpoint = 0 + (index*chunks)
        total_chunks = index + 1
        temp = function_to_apply(chunk)
        write_to_stream(stream, temp)


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
       Alternative len function that will simply return numpy.NA for invalid values 
       This is need to get sensible results when running len over a column that may contain nulls
    """
    try:
        return len(val)
    except:
        return np.nan

########################################################################################
def isNaN(num):
    return num != num


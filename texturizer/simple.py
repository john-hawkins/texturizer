# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np
import math
import os

from .config import max_filesize
 
"""
    texturizer.simple: Basic text feature calculation
"""


########################################################################################
def summarize_text(df, column):
    """
        Given a pandas dataframe and a column name.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    return rez


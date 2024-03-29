import sys
import pytest
import pandas as pd
import numpy as np
from texturizer.process import padded
from texturizer.process import extract_file_extension
from texturizer.process import count_lines
from texturizer.process import isNaN
from texturizer.process import remove_urls_and_tags
from texturizer.process import remove_urls
from texturizer.process import remove_tags
from texturizer.process import remove_escapes_and_non_printable

from texturizer.simple import add_text_features

def test_padded():
    strrez = padded("sdf", 20)
    assert len(strrez) == 20
    strrez = padded("sdf", 30)
    assert len(strrez) == 30


def test_extract_file_extension():
    ext = extract_file_extension("./test_functions.py")
    assert ext == ".py"


def test_count_lines():
    lines = count_lines("./tests/EXAMPLE.txt")
    assert lines == 5


def test_isNaN():
    assert isNaN(20) == False
    assert isNaN(20.0) == False
    assert isNaN(np.nan) == True

def test_simple():
    df = pd.DataFrame({'ID':[1,2,3], "text":["First Text", "Test two. Multi sentence.","Third.\nMulti line"]})
    rez =  add_text_features(df, "text")
    assert rez["text_wc"][0] == 2
    assert rez["text_wc"][1] == 4
    assert rez["text_wc"][2] == 3
    assert rez["text_sc"][0] == 1
    assert rez["text_sc"][1] == 2
    assert rez["text_sc"][2] == 2




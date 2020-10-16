import timeit
###############################################################################
# TEST THE EFFICIENCY OF MULTIPLE WAYS TO ADD CHAR PATTERN MATCHING FEATURES
#
# This test makes it very clear that using apply with counting the word matches
# is highly inefficient.
# The use of .loc with matching and an indicator variable is vectorized and over
# an order of magnitude faster.
###############################################################################
SETUP_CODE = """\
import pandas as pd
import re
df = pd.read_csv('../data/yahoo_answers.csv')
pattern = '\\bbasketball\\b|\\bbaseball\\b|\\bfootball\\b|\\bgolf\\b'
pattern2 = '\\bChristi|\\bchristi|\\bIslam|\\breligion\\b|\\bGod\\b|\\prayer'
matcher = re.compile(pattern)

def features(x, col):
    matches = 0
    if x[col]!=x[col]:
        matches = 0
    else:
        text = (x[col].lower())
        if len(matcher.findall(text)) > 0:
            matches = 1
    return matches

col='question'
"""
  
TEST_CODE = """\
df[col+'_matches'] = df.apply(features, col=col, axis=1)
"""

times = timeit.repeat(setup = SETUP_CODE, stmt = TEST_CODE, number = 5) 

print("Apply Time:", times)

TEST_CODE2 = """\
df.loc[df[col].str.contains(pattern), 'matches2'] = 1
""" 
times2 = timeit.repeat(setup = SETUP_CODE, stmt = TEST_CODE2, number = 5)

print("Loc Time:", times2 )


TEST_CODE3 = """\
df['sport_matches'] = df[col].str.count(pattern)
""" 
times3 = timeit.repeat(setup = SETUP_CODE, stmt = TEST_CODE3, number = 5)

print("Count Time:", times3 )

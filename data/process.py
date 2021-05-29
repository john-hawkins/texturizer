import pandas as pd
import numpy as np
import json

df = pd.read_csv("unigram_freq.csv")

# Take the square root count multiple times
# so that the scarcity range is logarithmic
df['count'] = np.sqrt(df['count'])
df['count'] = np.sqrt(df['count'])

total = sum(df['count'])

df['scarcity'] = 1 - (df['count']/total)

# Now scale between 0 and 1
lb = min(df['scarcity'])
denom = 1.0 - lb
df['scarcity'] =  (df['scarcity']-lb)/denom 

df.drop('count', inplace=True, axis=1)
rez = dict(df.values)


with open('../texturizer/data/scarcity.dat', 'w') as file:
     file.write(json.dumps(rez))



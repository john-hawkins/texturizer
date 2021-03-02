import pandas as pd

path_to_file = "~/Downloads/AFINN/AFINN-111.txt"

df = pd.read_csv(path_to_file, sep="\t", header=None)
df.columns = ['word','polarity']

df_pos = df[ df['polarity']>2 ].copy()
df_pos.drop(['polarity'], inplace=True, axis=1)
df_pos.to_csv("../texturizer/data/positive.dat",header=False,index=False)
 
df_neg = df[ df['polarity']<-2 ].copy()
df_neg.drop(['polarity'], inplace=True, axis=1)
df_neg.to_csv("../texturizer/data/negative.dat",header=False,index=False)
 


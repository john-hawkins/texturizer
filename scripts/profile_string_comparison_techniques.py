import pandas as pd
import numpy as np
import sys
import jellyfish
import textdistance
import string
import timeit
import random
import datetime as dt

def get_random_text(length):
    temp = [ random.choice(string.printable) for i in range(length)] 
    return ''.join(temp)

jd_time=[]
ld_time=[]
ji_time=[]
sd_time=[]
ro_time=[]

for i in range(50000): 
    raw_text1 = get_random_text( random.randint(100,200) )
    raw_text2 = get_random_text( random.randint(100,200) ) 
    #start = timeit.timeit()
    n1=dt.datetime.now()
    jd = jellyfish.jaro_distance(raw_text1,raw_text2)
    n2=dt.datetime.now()
    jd_time.append((n2-n1).microseconds)
    #end = timeit.timeit()
    #jd_time.append(end - start)

    #start = timeit.timeit()
    n1=dt.datetime.now()
    ld = jellyfish.levenshtein_distance(raw_text1,raw_text2)
    n2=dt.datetime.now()
    ld_time.append((n2-n1).microseconds)
    #end = timeit.timeit()
    #ld_time.append(end - start)

    #start = timeit.timeit()
    n1=dt.datetime.now()
    ji = textdistance.jaccard(raw_text1,raw_text2)
    n2=dt.datetime.now()
    ji_time.append((n2-n1).microseconds)
    #end = timeit.timeit()
    #ji_time.append(end - start)

    #start = timeit.timeit()
    n1=dt.datetime.now()
    sd = textdistance.sorensen(raw_text1,raw_text2 )
    n2=dt.datetime.now()
    sd_time.append((n2-n1).microseconds)
    #end = timeit.timeit()
    #sd_time.append(end - start)

    #start = timeit.timeit()
    n1=dt.datetime.now()
    ro = textdistance.ratcliff_obershelp(raw_text1,raw_text2)
    n2=dt.datetime.now()
    ro_time.append((n2-n1).microseconds)
    #end = timeit.timeit()
    #ro_time.append(end - start)
    
print("jellyfish.jaro_distance")
print( sum(jd_time)/50000 ) 

print("jellyfish.levenshtein_distance")
print( sum(ld_time)/50000 ) 

print("textdistance.jaccard")
print( sum(ji_time)/50000 ) 

print("textdistance.sorensen")
print( sum(sd_time)/50000 ) 

print("textdistance.ratcliff_obershelp")
print( sum(ro_time)/50000 ) 


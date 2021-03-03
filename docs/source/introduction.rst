Introduction
============

``Texturizer`` is a Python package which aims to provide an easy and intuitive way 
of generating features from columns of text in a dataset. 

The current implementation has been developed in Python 3 and tested on a variety of
CSV files. 


Motivation
**********

Text data can add significant value to machine learning projects, but it is not always
obvious how to make use of it. There are a vast number of ways to exploit text as features
in a model and it is not always clear what is likely to work.

This package is intended to provide a quick, as well as easily extensible framework to
add columns to a dataset using a wide variety of feature engineering approaches.


Limitations
***********

- The vast majority of these features are managed via RegEx patterns.


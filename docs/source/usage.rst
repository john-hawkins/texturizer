Usage Guide
===========


Command Line Utility
^^^^^^^^^^^^^^^^^^^^

Texturizer can be invoked from the command line:

.. code-block:: bash

    >texturizer


Without parameters it will print out an error and the following usage :


.. code-block:: bash

   ERROR: MISSING ARGUMENTS
   USAGE 
   /anaconda3/bin/texturizer  [ARGS] <PATH TO DATASET>
     <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf
    [ARGS] In most cases these are switches that turn on the feature type
     -columns=<COMMA SEPARATED LIST>. REQUIRED
     -topics            Default: False. Indicators for words from common topics.
     -topics=count                      Count matching words from common topics.
     -topics=normalize                  Count matching topic key words and normalize over topics.
     -traits            Default: False. Word usage for personality traits.
     -reason            Default: False. Word usage for reasoning: premises, conclusions.
     -rhetoric          Default: False. Word usage for rhetorical devices.
     -pos               Default: False. Part of speech proportions.
     -literacy          Default: False. Checks for simple literacy markers.
     -profanity         Default: False. Profanity check flags.
     -sentiment         Default: False. Words counts for positive and negative sentiment.
     -scarcity          Default: False. Word scarcity scores.
     -emoticons         Default: False. Emoticon check flags.
     -embedding         Default: False. Aggregate of Word Embedding Vectors.
     -embedding=normalize               Normalised Aggregate of Word Embedding Vectors.
     -comparison        Default: False. Cross-column comparisons using edit distances.


The list of columns to process and the path to the dataset are both mandatory.

The rest of the options turn on or off particular groups of features.

The package will output a computation time profile for all the feature sets it computes.
It is worthwhile running it over a sample of your data first to identofy features that may
be too computationally intensive for your data.


Python Package Usage
^^^^^^^^^^^^^^^^^^^^

You can import the texturize package within python and then make use of the
SciKit Learn Compatible Transformer for your ML Pipeline.
In the example below we initialise a TextTransform object that will generate
the literacy and topics indicator variables for any
dataframe that has a column of text named 'TEXT_COL_NAME'


.. code-block:: python

    from texturizer.pipeline import TextTransform
    from sklearn.linear_model import SGDClassifier
    from sklearn.pipeline import Pipeline

    pipeline = Pipeline([
        ('texttransform', TextTransform(['TEXT_COL_NAME'],['literacy','topics']) ),
        ('clf', SGDClassifier(loss='log') ),
    ])

Note that the transformer version of texturizer will remove the original text columns
so that the resulting data set can be fed into an algorithm that requires numerical 
columns only. This means that if you need to do any other text feature engineering it
be placed earlier in the pipeline.

 

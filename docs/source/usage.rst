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
     -topics OR -topics=count. Default: False. Match words from common topics (or count matches).
     -traits Default: False. Word usage for personality traits.
     -rhetoric Default: False. Word usage for rhetorical devices.
     -pos Default: False. Part of speech proportions.
     -literacy Default: False. Checks for common literacy markers.
     -profanity Default: False. Profanity check flags.
     -sentiment Default: False. Words counts for positive and negative sentiment.
     -emoticons Default: False. Emoticon check flags.
     -comparison Default: False. Cross-column comparisons.


The list of columns to process and the path to the dataset are both mandatory.

The rest of the options turn on or off particular groups of features.

Python Package Usage
^^^^^^^^^^^^^^^^^^^^

You can import the texturize package within python and then make use of the
SciKit Learn Compatible Transformer for your ML Pipeline.
In the example below we initialise a TextTransform object that will generate
the part of speech (pos), sentiment an topics indicator variables for any
dataframe that has a column of text named 'TEXT_COL_NAME'

.. code-block:: python

    import texturizer as txzr
    textTransformer = txzr.TextTransform(['TEXT_COL_NAME'],['pos','sentiment','topics'])



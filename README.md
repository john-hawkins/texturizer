texturizer
----------

```
Status - Functional
```
Initial Working Version for in-memory datasets

This is an application to add features to a dataset that are derived from processing
the content of existing columns of text data.

It will accept a CSV, TSV or XLS file and output an extended version of
the dataset with additional columns appended. When run with default settings
it will produce very simple and rapid numerical summaries. Additional feature
flags unlock deeper NLP based features that are more computationally intensive.


### TODO

```
* Build functionality to process large datasets in chunks.
* Add capacity to generate features relative to corpus averages
* Add capacity for comparison features to be generated relative to reference text(s)
* Add functionality for working with unix shell pipes and streams
```

### Distribution

Released and distributed via setuptools/PyPI/pip for Python 3.

Built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)


### Resources & Dependencies

For Part of Speech Tagging we use [spacy](https://spacy.io/usage/spacy-101)

Note: After install you will need to get spaCy to download the English model.
```
sudo python3 -m spacy download en
```
For string based text comparisons we use [jellyfish](https://pypi.org/project/jellyfish/) and
[textdistance](https://pypi.org/project/textdistance/)

## Features

Each type of feature can be unlocked through the use of a specific command line switch:

* -topics. Indicators for presence of words from common topics.
* -topics=count. Counts of all word matches from common topics.
* -pos. Part of speech proportions in the text.
* -literacy. Checks for common literacy markers.
* -traits. Checks for common stylistic elements or traits that suggest personality type.
* -profanity. Profanity check flags.
* -sentiment. Sentiment word counts and score.
* -emoticons. Emoticon check flags.
* -comparison. Cross-column comparisons using edit distance metrics

## Usage

You can use this application multiple ways

Use the runner without installing the application. 
The following example will generate all features on the test data.

```
./texturizer-runner.py -columns=question,answer -pos -literacy -traits -profanity -emoticons -sentiment -comparison -topics=count data/test.csv > data/output.csv
```

This will send the time performance profile to STDERR as shown below:
```
Computation Time Profile for each Feature Set
---------------------------------------------
simple               0:00:00.521356
comparison           0:00:00.460415
profanity            0:00:00.461585
sentiment            0:00:01.429136
emoticons            0:00:00.373074
topics               0:00:02.685745
traits               0:00:02.082641
pos                  0:00:20.773449
literacy             0:00:00.481656
```  
As you can see the part of speech (POS) features are the most time 
consuming to generate. It is worth avoiding them on very large datasets.

Alternatively, you can invoke the directory as a package:
 
```
python -m texturizer -columns=question,answer data/test.csv > data/output.csv
```

Or simply install the package and use the command line application directly


# Installation
Installation from the source tree:

```
python setup.py install
```

(or via pip from PyPI):

```
pip install texturizer
```

You will then need to run the [POST_INSTALL.sh](POST_INSTALL.sh) script to install
the required Spacy Model (otherwise the POS features cannot be calculated).


Now, the ``texturizer`` command is available::

```
texturizer -columns=question,answer -topics data/test.csv > data/output.csv
```

This will produce take the [Input CSV](data/test.csv), add simple summary columns and 
produce an Output CSV with features appended as new columns.

For more complicated features see the additional options.


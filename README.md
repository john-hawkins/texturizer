texturizer
----------

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/john-hawkins/texturizer/actions/workflows/python-package.yml/badge.svg)](https://github.com/john-hawkins/texturizer/actions/workflows/python-package.yml)
[![PyPI](https://img.shields.io/pypi/v/texturizer.svg)](https://pypi.org/project/texturizer)
[![Documentation Status](https://readthedocs.org/projects/texturizer/badge/?version=latest)](https://texturizer.readthedocs.io/en/latest/?badge=latest)

```
Status - Functional
```

This is an application to add features to a dataset that are derived from processing
the content of existing columns of text data. It is specifically designed for adding
somewhat bespoke and unusual features that are not particularly well identified by
n-gram or word embedding approaches.

It will accept a CSV, TSV or XLS file and output an extended version of
the dataset with additional columns appended. When run with default settings
it will produce a small number of very simple numerical summaries. 

Additional feature flags unlock features that are more computationally intensive and
generally domain specific.

Released and distributed via setuptools/PyPI/pip for Python 3.

Additional detail available in the [documentation](https://texturizer.readthedocs.io)

### TODO

```
Current features are all derived from single records. Future development will add these
in some sense relative to a corpus.

* Add capacity to generate features relative to corpus averages
* Add capacity for comparison features to be generated relative to reference text(s)
* Investigate functionality for working with unix shell pipes and streams

```

### Distribution

Released and distributed via setuptools/PyPI/pip for Python 3.


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
* -rhetoric. Checks for rhetorical devices used for persuasion
* -profanity. Profanity check flags.
* -sentiment. Sentiment word counts and score.
* -emoticons. Emoticon check flags.
* -comparison. Cross-column comparisons using edit distance metrics

## Usage

You can use this application multiple ways

Use the runner without installing the application. 
The following example will generate all features on the test data.

```
./texturizer-runner.py -columns=question,answer -pos -literacy -traits -rhetoric -profanity -emoticons -sentiment -comparison -topics=count data/test.csv > data/output.csv
```

This will send the time performance profile to STDERR as shown below:
```
Computation Time Profile for each Feature Set
---------------------------------------------
simple               0:00:00.580910
comparison           0:00:00.490972
profanity            0:00:00.507172
sentiment            0:00:03.611817
emoticons            0:00:00.387556
topics               0:00:02.778537
traits               0:00:00.262633
rhetoric             0:00:02.107620
pos                  0:00:22.130724
literacy             0:00:00.488886
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

You will then need to run the [POST INSTALL SCRIPT](https://github.com/john-hawkins/texturizer/blob/master/POST_INSTALL.sh) to install the required Spacy Model (otherwise the POS features cannot be calculated).
 

Now, the ``texturizer`` command is available::

```
texturizer -columns=question,answer -topics data/test.csv > data/output.csv
```

This will take the Input CSV, calculate some simple summary features and 
produce an Output CSV with features appended as new columns.

For more complicated features see the additional options (outlined above).

# Acknowledgements

Python package built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)



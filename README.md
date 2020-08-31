texturizer
----------

```
Status - Functional: Initial Working Version for in-memory datasets

TODO:

* Build functionality to process large datasets in chunks.
* Add capacity to generate features relative to corpus averages
* Add capacity for comparison features to be generated relative to refence text
* Add functionality for working with unix shell pipes and streams
* Improve emoticon handling to demarcate sentiment
* Improve topic features to be based on external reference lists of unambiguous words
```

This is an application to add features to a dataset that are derived from analysis of
the content of existing columns of text data.

It will accept a CSV, TSV or XLS file and output an extended version of
the dataset with additional columns appended. When run with default settings
it will produce very simple and rapid numerical summaries. Additional feature
flags unlock deeper NLP based features that are more computationally intensive.

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

Use the runner:

```
./texturizer-runner.py -columns=question,answer  -topics data/test.csv > data/output.csv
```

Invoke the directory as a package:

```
python -m texturizer -columns=question,answer data/test.csv
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

Now, the ``texturizer`` command is available::

```
texturizer -columns=question,answer -topics data/test.csv > data/output.csv
```

This will produce take the [Input CSV](data/test.csv), add simple summary columns and 
produce the [Output CSV](data/output.csv)

For more complicated features see the additional options.



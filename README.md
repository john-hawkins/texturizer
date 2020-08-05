texturizer
----------

```
Status - Incomplete
```

This is an application to add text based features to a dataset.

It will accept a CSV, TSV or XLS file and output an extended version of
the dataset with additional columns appended. When run with default settings
it will produce very simple and rapid numerical summaries. Additional feature
flags unlock deeper NLP based features that are more computationally intensive.

Released and distributed via setuptools/PyPI/pip for Python 3.

Built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)

### TODO

### Resources

I will be using a combination of [spacy](https://spacy.io/usage/spacy-101) and NLTK


## Usage

You can use this application multiple ways

Use the runner:

```
./texturizer-runner.py markdown data/test.csv > markdown_test.md
```

Which was used to generate the markdown [output test file](markdown_test.md)

Invoke the directory as a package:

```
python -m texturizer markdown data/test.csv
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
texturizer data/test.csv > data/output.csv
```

This will produce take the [Input CSV](data/test.csv), add simple summary columns and 
produce the [Output CSV](data/output.csv)

For more complicated NLP derived features see the additional options.


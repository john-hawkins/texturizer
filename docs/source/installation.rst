Installation
============

The Texturizer package is maintained inside the PyPi package manager.

Install the from PyPi as follows:

.. code-block:: bash

    pip install texturizer

Alternatively, you can access the source code for MinViME and use it 
by installing it locally:

.. code-block:: bash

    git clone https://github.com/john-hawkins/texturizer.git
    cd texturizer
    python setup.py install


The core functions in Texturizer depend on the following packages:

.. code-block:: bash

    numpy>=1.16.4
    pandas>=0.25.3
    jellyfish
    textdistance
    spacy
    textblob

Some features will also require an installation of the SpacY language file: "en_core_web_sm"

.. code-block:: bash

    sudo python3 -m spacy download en


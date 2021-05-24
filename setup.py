# -*- coding: utf-8 -*-
 
"""setup.py: setuptools control."""
 
import re
from setuptools import setup
 
version = re.search(
        '^__version__\s*=\s*"(.*)"',
        open('texturizer/__init__.py').read(),
        re.M
    ).group(1)
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
      license="MIT",
      name = "texturizer",
      packages = ["texturizer"],
      install_requires=[
        'pandas','numpy','sklearn','jellyfish','textdistance','spacy','textblob'
      ],
      include_package_data=True,
      entry_points = {
        "console_scripts": ['texturizer = texturizer.texturizer:main']
      },
      version = version,
      description = "Python command line application to add text features to a CSV or TSV dataset.",
      long_description = long_descr,
      long_description_content_type='text/markdown',
      author = "John Hawkins",
      author_email = "johnc@getting-data-science-done.com",
      url = "http://john-hawkins.github.io",
      project_urls = {
          'Documentation': "http://texturizer.readthedocs.io",
          'Source': 'https://github.com/john-hawkins/texturizer',
          'Tracker': 'https://github.com/john-hawkins/texturizer/issues',
      },
    )



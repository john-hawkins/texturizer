#!/bin/bash

# ##############################################################
# Set-up the environment for NLP Scripts
# ##############################################################
conda env create -f nlp_course_env.yml

source activate nlp_course

# For some reason this was not in the environment
pip install PyPDF2

# Install the word embedding vector library -- Large Download
python -m spacy download en_core_web_lg



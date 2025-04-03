# Machine Learning Project [Group 6]: Final Project
#### Cody van der Deen, Dies de Haan, Isa Houtsma, Jasper Wieten

This repository contains all code used and created for the 2025 MLP Final Project.

## Requirements
- Numpy
- Pandas
- NLTK
- Scikit-learn
- matplotlib

## Usage
First and foremost, all data files (in this case, these should always be .conll files) must be stored in a folder named "data" (not tracked in this repository).
To run for the final results, as documented in the paper, only **run_final.py** should be used. However, classify_SVM.py and collect_and_process.py can also be run independently.
These will run the classifier on a single file or split the data and output it to different files, respectively.

## Getting your API keys for dictionary lookup
To start, you must obtain Merriam-Webster API keys. These can be obtained by registering for a developer account:

1. Go to this website: https://dictionaryapi.com/register/index
2. Register for a developer account.
3. When you reach the checkboxes "Request API Key (1)" and "Request API Key (2)", select "Collegiate Dictionary" for English, and "Spanish-English Dictionary" for Spanish.
4. Confirm your email address.
5. Log into your account and go to "Your Keys".
7. Copy your keys (the direct string, not JSON or PHP) and paste them into apikey.py.
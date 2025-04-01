# File name: english_classifier.py
# Authors: D. de Haan, S6186408
# Date: 27-03-2025

import requests
import os
from apikey import ENGLISH_API_KEY
import re
import atexit
import json

# cache to avoid double api's
CACHE_FILE = "eng_seen.json" 
try:
    with open(CACHE_FILE, "r") as f:
        seen = json.load(f)
except FileNotFoundError:
    seen = {}

def clean_token(token):
    """delete reading signs, 
    and convert to lowercase to make it easy to proces"""
    token = token.lower()
    
    # Keep english letters
    token = re.sub(r'[^\wáéíóúüñ]', '', token)
    return token

def is_english(word):
    """Return True if word english according the Merriam-Webster english API."""
    try:
        en_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={ENGLISH_API_KEY}"
        en_response = requests.get(en_url, timeout=5)

        if en_response.status_code != 200:
            # only uncomment to see the results of the api call
            #print(f"False: status {en_response.status_code} for word '{word}'")
            return False

        en_data = en_response.json()

        # only uncomment to see the results of the word search and the answer
        #print(f"\n Check: {word}")
        #print(f"Answer: {en_data if len(en_data) > 0 else 'No result'}")

        return isinstance(en_data, list) and len(en_data) > 0 and isinstance(en_data[0], dict)

    except requests.exceptions.RequestException as e:
        # only uncomment to see the results of connection error
        #print(f"Connection error'{word}': {e}")
        return False
    except ValueError:
        # only uncomment to see the results of json error
        #print(f"JSON decode fault for '{word}'. possibly no valid response.")
        return False

# print the results to an other file
def classify_conll_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            stripped = line.strip()
            if stripped == "":
                outfile.write("\n")
                continue

            raw_token = stripped.split()[0]
            token = clean_token(raw_token)

            if token not in seen:
                seen[token] = is_english(token)
            
            label = "lang1" if seen[token] else None
            outfile.write(f"{token}\t{label}\n")

def classify(word):
    word = clean_token(word)
    if word in seen:
        return seen[word]
    result = "lang1" if is_english(word) else None  # (or "lang2" for Spanish)
    seen[word] = result
    return result

# write cache to an other file to make it faster
@atexit.register
def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(seen, f)
    print(f"[{__name__}] Saved {len(seen)} words to cache.")

if __name__ == "__main__":
    input_file = os.path.join("data", "test.conll")
    output_file = os.path.join("data", "test_eng_classified_.conll")
    
    print("Busy classifying tokens.")

    # only uncomment when wanting to see if want the output 
    # to go to an external file, and see when ready
    #classify_conll_file(input_file, output_file)
    #print(f"\n Ready {output_file}")


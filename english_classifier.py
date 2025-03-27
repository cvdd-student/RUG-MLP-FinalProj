import requests
import os
from apikey import ENGLISH_API_KEY
import re

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
        es_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={ENGLISH_API_KEY}"
        es_response = requests.get(es_url, timeout=5)

        if es_response.status_code != 200:
            print(f"False: status {es_response.status_code} for word '{word}'")
            return False

        es_data = es_response.json()

        print(f"\n Check: {word}")
        print(f"Answer: {es_data if len(es_data) > 0 else 'No result'}")

        return isinstance(es_data, list) and len(es_data) > 0 and isinstance(es_data[0], dict)

    except requests.exceptions.RequestException as e:
        print(f"Connection error'{word}': {e}")
        return False
    except ValueError:
        print(f"JSON decode fault for '{word}'. possibly no valid response.")
        return False

def classify_conll_file(input_path, output_path):
    seen = {}  # cache to avoid double api's
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
            
            label = "True" if seen[token] else "False"
            outfile.write(f"{token}\t{label}\n")

if __name__ == "__main__":
    input_file = os.path.join("data", "test.conll")
    output_file = os.path.join("data", "test_eng_classified_.conll")
    
    print("Busy classifying tokens from test.conll...")
    classify_conll_file(input_file, output_file)
    print(f"\n Ready {output_file}")


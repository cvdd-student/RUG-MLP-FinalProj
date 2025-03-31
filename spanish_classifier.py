import requests
import os
from apikey import SPANISH_API_KEY
import re

def clean_token(token):
    """delete reading signs, 
    and convert to lowercase to make it easy to proces"""
    token = token.lower()
    
    # Keep spanish letters
    token = re.sub(r'[^\wáéíóúüñ]', '', token)
    return token

def is_spanish(word):
    """Return True if word spanish according the Merriam-Webster spanish API."""
    try:
        es_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={SPANISH_API_KEY}"
        es_response = requests.get(es_url, timeout=5)

        if es_response.status_code != 200:
            # only uncomment to see the results of the api call
            #print(f"False: status {es_response.status_code} for word '{word}'")
            return False

        es_data = es_response.json()

        # # only uncomment to see the results of the word search and the answe
        #print(f"\n Check: {word}")
        #print(f"Answer: {es_data if len(es_data) > 0 else 'No result'}")

        return isinstance(es_data, list) and len(es_data) > 0 and isinstance(es_data[0], dict)

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
                seen[token] = is_spanish(token)
            
            label = "lang2" if seen[token] else None
            outfile.write(f"{token}\t{label}\n")

def classify(word):
    word = clean_token(word)
    return "lang2" if is_spanish(word) else None

if __name__ == "__main__":
    input_file = os.path.join("data", "test.conll")
    output_file = os.path.join("data", "test_classified.conll")
    
    print("Busy classifying tokens from test.conll...")

    # only uncomment when wanting to see if want the output 
    # to go to an external file, and see when ready
    #classify_conll_file(input_file, output_file)
    #print(f"\n Ready {output_file}")

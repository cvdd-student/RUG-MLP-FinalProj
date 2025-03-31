# File name: DICTengspaAPI.py
# Authors: D. de Haan, S6186408
# Date: 20-03-2025

import requests

ENGLISH_API_KEY = "de514aa6-86c0-421d-a5d1-3ffe1cd9f83e"  # API key english
SPANISH_API_KEY = "e0d53114-debc-4211-ae43-12066118ab75"  # API key spanish

def check_language(word):
    """Check if a word is English or Spanish using the Merriam-Webster API."""
    # Check English dictionary
    eng_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={ENGLISH_API_KEY}"
    eng_response = requests.get(eng_url)
    
    # Check Spanish dictionary
    es_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={SPANISH_API_KEY}"
    es_response = requests.get(es_url)

    eng_data = eng_response.json()
    es_data = es_response.json()

    print(f"\n🔍 Checking word: {word}")
    print(f"English response: {eng_data if len(eng_data) > 0 else 'No match'}")
    print(f"Spanish response: {es_data if len(es_data) > 0 else 'No match'}")

    # Determine category
    if isinstance(eng_data, list) and len(eng_data) > 0 and isinstance(eng_data[0], dict):
        return "Engels"
    elif isinstance(es_data, list) and len(es_data) > 0 and isinstance(es_data[0], dict):
        return "Spaans"
    else:
        return "Onbekend"

# Word list
word_list = ["apple", "perro", "house", "gato", "cielo", "unknownword", "playa", "amor", "sambal"]

# Categorize words
categorized_words = {"Engels": [], "Spaans": [], "Onbekend": []}

for word in word_list:
    category = check_language(word)
    categorized_words[category].append(word)

# Show results
print("\n✅ Gecategoriseerde woorden:")
for category, words in categorized_words.items():
    print(f"{category}: {', '.join(words)}")
import requests

# Vervang deze met je eigen API-sleutels
ENGLISH_API_KEY = "your_english_api_key"  # API sleutel voor Engels
SPANISH_API_KEY = "your_spanish_api_key"  # API sleutel voor Spaans

def check_language(word):
    """Controleert of een woord Engels of Spaans is via de Merriam-Webster API."""
    # Controleer Engels woordenboek
    eng_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={ENGLISH_API_KEY}"
    eng_response = requests.get(eng_url)
    
    # Controleer Spaans woordenboek
    es_url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={SPANISH_API_KEY}"
    es_response = requests.get(es_url)
    
    if eng_response.status_code == 200 and isinstance(eng_response.json(), list) and len(eng_response.json()) > 0:
        return "Engels"
    elif es_response.status_code == 200 and isinstance(es_response.json(), list) and len(es_response.json()) > 0:
        return "Spaans"
    else:
        return "Onbekend"

# Woordenlijst hier aansluiten nu een dummy waarde
word_list = ["apple", "perro", "house", "gato", "cielo", "unknownword", "playa", "amor",'sambal']

# Woordenlijst hier aansluiten nu een dummy waarde
categorized_words = {"Engels": [], "Spaans": [], "Onbekend": []}

for word in word_list:
    category = check_language(word)
    categorized_words[category].append(word)

# Resultaten weergeven
print("Gecategoriseerde woorden:")
for category, words in categorized_words.items():
    print(f"{category}: {', '.join(words)}")

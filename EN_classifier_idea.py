import nltk
from nltk.corpus import words
from abs_custom_classifier_with_feature_generator import CustomClassifier
import numpy as np

# Ensure that the NLTK words corpus is downloaded
nltk.download('words')

class EN_Dic_classifier(CustomClassifier):
    def __init__(self):
        super().__init__()
        self.EN_words = set(words.words())  # Load English words into a set for fast lookup

    def get_features(self, test_items, features_vocab=None, ngram=1):
        """Convert word presence into a NumPy feature array for ML compatibility."""
        return np.array([[1 if word.lower() in self.EN_words else 0] for word in test_items])

    def fit(self, train_features, train_labels):
        """No training needed, method kept for compatibility."""
        pass

    def predict(self, test_items):
        """Predict using the feature extraction method."""
        return self.get_features(test_items).flatten()

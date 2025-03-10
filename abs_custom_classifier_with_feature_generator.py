import abc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import numpy as np

"""
Implement a classifier with required functions:

get_features: should return a feature vector
for each sample (1-hot, n-hot encodings or etc.)

fit: to train the classifier
predict: to predict test labels
"""


class CustomClassifier(abc.ABC):
    def __init__(self):
        self.counter = None

    def get_feature_vocab(self, text_list, ngram=1):
        """ Return a vocabulary from the text list provided as a python dict
        with the key being the word/ngram and the value being the index.
        A dictionary is used for efficiency."""

        features_vocab = dict()
        index_vocab = 0

        # Build vocab
        for text in text_list:
            for i in range(len(text) - (ngram - 1)):
                if ngram > 1:
                    feature_item = []
                    for n in range(ngram):
                        feature_item.append(text[i+n])
                    feature_item = tuple(feature_item)
                else:
                    feature_item = text[i]
                if feature_item not in features_vocab:
                    features_vocab[feature_item] = index_vocab
                    index_vocab += 1

        return features_vocab

    def get_features(self, text_list, features_vocab, ngram=1):
        """ Return word (or ngram) count features
        for each text as a 2D numpy array """

        features_array = []

        # Create hot encodings
        for text in text_list:
            text_encodings = np.zeros(len(features_vocab))
            for i in range(len(text) - (ngram - 1)):
                # Create tuples if not unigrams
                if ngram > 1:
                    feature_item = []
                    for n in range(ngram):
                        feature_item.append(text[i+n])
                    feature_item = tuple(feature_item)
                # Just use the string for unigrams
                else:
                    feature_item = text[i]
                if feature_item in features_vocab:
                    text_encodings[features_vocab[feature_item]] += 1
            features_array += [text_encodings]

        features_array = np.array(features_array)
        features_array = self.tf_idf(features_array)

        return features_array

    def tf_idf(self, text_feats):
        tfidf_transformer = TfidfTransformer().fit(text_feats)
        return tfidf_transformer.transform(text_feats)

    @abc.abstractmethod
    def fit(self, train_features, train_labels):
        """ Abstract method to be separately implemented
        for each custom classifier. """
        pass

    @abc.abstractmethod
    def predict(self, test_features):
        """ Abstract method to be separately implemented
        for each custom classifier. """
        pass

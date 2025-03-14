import os
import numpy as np
import pandas as pd
import time
import random
from sklearn import metrics
from sklearn_svm_classifier import SVMClassifier

def split_labelled(data, setlen=0, flag_shuffle=False):
    print("SPLITTING DATASET...")
    list_split = []
    pos_enum = 0

    for line in data.split("\n"):
        if line == "":
            pos_enum += 1
        elif line[:11] == "# sent_enum":
            pass
        elif line[0] == "#":
            pass
        else:
            line_export = line.split("\t")
            try:
                list_split[pos_enum].append(line_export)
            except IndexError:
                list_split.append([line_export])

    if flag_shuffle == True:
        random.shuffle(list_split)

    print("OK")
    
    if setlen == 0:
        return list_split
    else:
        return list_split[:setlen]


def split_test(data):
    print("SPLITTING SET")
    list_export = []
    for line in data.split("\n"):
        if line != "":
            list_export.append(line)

    return list_export


def train_test(train_items, train_labels, test_items):
    cls = SVMClassifier(kernel='linear')
    feats_vocab = cls.get_feature_vocab(train_items, 1)
    train_feats = cls.get_features(train_items, feats_vocab, 1)
    test_feats = cls.get_features(test_items, feats_vocab, 1)

    print("FITTING MODEL...")
    cls.fit(train_feats, train_labels)
    print("OK")

    print("PREDICTING...")
    predicted_test_labels = cls.predict(test_feats)
    print("OK")
    
    return predicted_test_labels


def evaluate(true_labels, predicted_labels):
    """
    Print accuracy, precision, recall and f1 metrics for each class, and their macro average.
    """

    # Use confusion matrix generated by the provided function
    # to calculate evaluation metrics.
    confusion_matrix = metrics.confusion_matrix(y_true=true_labels, y_pred=predicted_labels)

    accuracy = metrics.accuracy_score(y_true=true_labels, y_pred=predicted_labels)
    precision = metrics.precision_score(y_true=true_labels, y_pred=predicted_labels, average='macro')
    recall = metrics.recall_score(y_true=true_labels, y_pred=predicted_labels, average='macro')
    f1score = metrics.f1_score(y_true=true_labels, y_pred=predicted_labels, average='macro')

    print('***** Evaluation *****')
    print("Accuracy: " + str(accuracy))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F1: " + str(f1score))
    print("\nConfusion matrix:\n" + str(confusion_matrix))


def main():
    with open("data/train.conll", "r") as file:
        raw_data = file.read()

    with open("data/dev.conll", "r") as file:
        raw_test_data = file.read()

    work_list = split_labelled(raw_data, 1000, True)
    test_list = split_labelled(raw_test_data)

    items = []
    labels = []
    test_items = []
    test_labels = []
    print("ORDERING TRAIN ITEMS/LABELS...")
    for sent in work_list:
        for item, label in sent:
            items.append(item)
            labels.append(label)
    print("OK")
    print("ORDERING TEST ITEMS/LABELS...")
    for sent in test_list:
        for item, label in sent:
            test_items.append(item)
            test_labels.append(label)
    print("OK")

    items = np.array(items)
    labels = np.array(labels)
    test_items = np.array(test_items)
    test_labels = np.array(test_labels)

    predict_labels = train_test(items, labels, test_items)

    evaluate(test_labels, predict_labels)

    filename = "result/labels_"
    filename += str(time.time())
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for item in predict_labels:
            file.write(str(item))
            file.write("\n")

main()

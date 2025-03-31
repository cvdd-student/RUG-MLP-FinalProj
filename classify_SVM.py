import collect_and_process
from sklearn import svm
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
import os
import numpy as np

def evaluate(true_labels, predicted_labels):
    '''Print accuracy, precision, recall and f1 metrics for each class, and their macro average.
    TODO: This should be removed/redone for the final project!!!!!!!'''

    baseline_labels = []
    for i in range(len(true_labels)):
        baseline_labels.append("lang1")
        
    confusion_matrix = metrics.confusion_matrix(y_true=true_labels, y_pred=baseline_labels)
    
    accuracy = metrics.accuracy_score(y_true=true_labels, y_pred=baseline_labels)
    precision = metrics.precision_score(y_true=true_labels, y_pred=baseline_labels, average='macro')
    recall = metrics.recall_score(y_true=true_labels, y_pred=baseline_labels, average='macro')
    f1score = metrics.f1_score(y_true=true_labels, y_pred=baseline_labels, average='macro')

    print('***** Evaluation BASELINE *****')
    print("Accuracy: " + str(accuracy))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F1: " + str(f1score))
    print("\nConfusion matrix:\n" + str(confusion_matrix))

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

    # Exporting the data behaviours
    print("NOTICE: Data being exported to export/eval folder!")
    filename = "export/eval/export_"
    filename += str(time.time())
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for line in predicted_labels:
            file.write(str(line))
            file.write("\n")


def convert_data_to_features(train_data, test_data):
    '''Converts the data to features, using CountVectorizer
    and TfidfTransformer, then returns the data.'''
    train_words = []
    test_words = []
    
    # Convert the lists to strings.
    # This is so the vectorizers can easily
    # incorporate the tag data.
    for item in train_data:
        train_words.append(" ".join(item))
    
    for item in test_data:
        test_words.append(" ".join(item))
    
    # Init count vec and create count vectors
    vec_count = CountVectorizer()
    vec_count.fit(train_words)
    train_count_vec = vec_count.transform(train_words)
    test_count_vec = vec_count.transform(test_words)
    
    # Init tdidf vec and create tfidf vectors
    vec_tfidf = TfidfTransformer()
    vec_tfidf.fit(train_count_vec)
    train_feats = vec_tfidf.transform(train_count_vec)
    test_feats = vec_tfidf.transform(test_count_vec)
    
    return train_feats, test_feats


def train_cls(train_feats, train_labels, test_feats):
    '''Initiate and fit a SVM classifier, then return
    the classifier.'''
    # Init the classifier, decide what type is the best.
    cls = svm.LinearSVC()  # Accuracy around 0.835 on dev dataset
    #cls = svm.SVC(decision_function_shape='ovo')    # Accuracy around 0.827 on dev dataset
    
    print("Training model...")
    cls.fit(train_feats, train_labels)
    print("OK")

    return cls


def main():
    data = collect_and_process.get_data()
    tr_items, tr_labels, te_items, te_labels = collect_and_process.collect_and_process(data)
    
    tr_feats, te_feats = convert_data_to_features(tr_items, te_items)
    
    cls = train_cls(tr_feats, tr_labels, te_feats)
    pred_labels = cls.predict(te_feats)
    evaluate(te_labels, pred_labels)


if __name__ == "__main__":
    main()

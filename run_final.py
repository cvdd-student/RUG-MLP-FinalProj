# File name: run_final.py
# Function: Runs the pre-processing and SVM classifier
# for the final results. WARNING: This uses ALL the data we
# have, so it will take a while to run!
# Authors: C. Van der Deen, S4092597
# Date: 31-03-2025

import collect_and_process
import classify_SVM

def main():
    print("PROGRESS: Opening files")
    with open("data/train.conll", "r") as file:
        train_data = file.read()
    with open("data/dev.conll", "r") as file:
        test_data = file.read()

    print("PROGRESS: Splitting data")
    train_data_list = collect_and_process.split_labelled(train_data)
    test_data_list = collect_and_process.split_labelled(test_data)

    print("PROGRESS: Adding POS & NE presence")
    train_process = collect_and_process.add_pos_ne_presence(train_data_list)
    test_process = collect_and_process.add_pos_ne_presence(test_data_list)

    print("PROGRESS: Separating data & labels")
    train_items, train_labels = collect_and_process.separate_data_labels(train_process)
    test_items, test_labels = collect_and_process.separate_data_labels(test_process)

    print("PROGRESS: Converting data to features")
    train_feats, test_feats = classify_SVM.convert_data_to_features(train_items, test_items)

    print("PROGRESS: Running classifier")
    cls = classify_SVM.train_cls(train_feats, train_labels, test_feats)

    print("PROGRESS: Generating predictions")
    pred_labels = cls.predict(test_feats)

    classify_SVM.evaluate(test_labels, pred_labels)


if __name__ == "__main__":
    main()
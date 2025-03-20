# File name: collect_and_process.py
# Function: Processes raw data (tab-separated tokens and labels)
# in several desired ways.
# Author: C. Van der Deen, S4092597
# Date: 11-03-2025

import os
import numpy as np
import pandas as pd
import time
import random
from math import ceil


def split_labelled(data, export_mode=False):
    '''Splits the given data (tab separated items & labels) into
    a list of lists, then returns it.'''
    list_split = []
    pos_enum = 0

    for line in data.split("\n"):
        if line == "":
            # An empty line is used to separate the sentences, so we
            # can use it to jump to the next sentence.
            pos_enum += 1
        elif line[:11] == "# sent_enum":
            # This needs to be this specific because of
            # used hashtags or loose hashtags.
            pass
        else:
            line_export = line.split("\t")
            # Add to the current sentence's list
            try:
                list_split[pos_enum].append(line_export)
            # If there is no list for the sentence yet
            except IndexError:
                list_split.append([line_export])

    if export_mode is False:
        return list_split

    # Exporting the data behaviours
    print("NOTICE: Data being exported to export/split_labelled folder!")
    filename = "export/split_labelled/export_"
    filename += str(time.time())
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for line in list_split:
            file.write(str(line))

    return list_split


def destroy_sent_divide(data, export_mode=False):
    '''Removes the sentence division between tokens.
    This loses data!'''
    list_export = []
    for line in data:
        list_export += line

    if export_mode is False:
        return list_export

    # Export behaviours
    print("NOTICE: Data being exported to export/destroy_sent_divide folder!")
    filename = "export/destroy_sent_divide/export_"
    filename += str(time.time())
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for line in list_export:
            file.write(str(line))
            file.write("\n")

    return list_export


def select_and_shuffle(data, total_items=-1, flag_train_test_split=False, test_percentage=20, flag_shuffle=False):
    '''Able to process the provided data in several ways, all optional:
    1. Can shuffle the data.
    2. Can split data into training and testing sets, based on a percentage.
    3. Can limit the total amount of items.'''
    if flag_shuffle:
        random.shuffle(data)

    if total_items != -1:
        data = data[:total_items]

    if flag_train_test_split:
        amt_test_items = ceil(len(data) * (test_percentage / 100))
        data_test = data[:amt_test_items]
        data_train = data[amt_test_items:]

    if flag_train_test_split:
        return data_train, data_test
    else:
        return data


def separate_data_labels(data, export_mode=False):
    '''Separates the items and labels, and exports them as separate lists.'''
    list_items = []
    list_labels = []
    for item, label in data:
        list_items.append(item)
        list_labels.append(label)

    if export_mode is False:
        return list_items, list_labels

    # Export behaviours
    print("NOTICE: Data being exported to export/separate_data_labels folder!")
    timestamp = time.time()

    filename = "export/separate_data_labels/items_"
    filename += str(timestamp)
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for item in list_items:
            file.write(str(item))
            file.write("\n")

    filename = "export/separate_data_labels/labels_"
    filename += str(timestamp)
    filename += ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for label in list_labels:
            file.write(str(label))
            file.write("\n")

    return list_items, list_labels


def file_select():
    '''Displays the files in the data folder,
    and returns the file chosen.'''
    files = os.listdir("data")
    for i in range(len(files)):
        filepath = "data/" + files[i]
        if os.path.isfile(filepath):
            print("[" + str(i) + "]", end=" ")
            print(files[i])

    selected_file_index = input("Which file would you like to process? (Type only number)\n")
    try:
        selected_file_index = int(selected_file_index)
    except ValueError:
        print("Invalid selection")
        exit()

    selected_file = files[selected_file_index]
    return "data/" + selected_file


def get_data():
    '''Gets a file from file_select() and returns it as read data.'''
    selected_file = file_select()
    with open(selected_file, "r") as file:
        data = file.read()
    return data


def export_processed_data(data, name, timestamp):
    '''Exports the provided data with the provided name and timestamp.'''
    filename = "processed/"
    filename += str(timestamp)
    filename += "/"
    filename += name
    filename += ".txt"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        for line in data:
            file.write(str(line))
            file.write("\n")


def collect_and_process(data):
    data_list = split_labelled(data)
    data_list = destroy_sent_divide(data_list)
    train_list, test_list = select_and_shuffle(data_list, total_items=-1, flag_train_test_split=True, flag_shuffle=True)

    train_items, train_labels = separate_data_labels(train_list)
    test_items, test_labels = separate_data_labels(test_list)

    return train_items, train_labels, test_items, test_labels


if __name__ == "__main__":
    data = get_data()
    tr_items, tr_labels, te_items, te_labels = collect_and_process(data)
    timestamp = time.time()
    export_processed_data(tr_items, "train_items", timestamp)
    export_processed_data(tr_labels, "train_labels", timestamp)
    export_processed_data(te_items, "test_items", timestamp)
    export_processed_data(te_labels, "test_labels", timestamp)

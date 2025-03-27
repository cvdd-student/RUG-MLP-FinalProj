from nltk import ne_chunk
from nltk.corpus import wordnet
import nltk

import collect_and_process
import time
import os

def get_ne_tags(items):
	ne_detections = []
	for word in items:
		word_tokenized = nltk.word_tokenize(word)
		word_pos = nltk.pos_tag(word_tokenized)
		word_ne = nltk.ne_chunk(word_pos)
		try:
			if word_ne[0].label():
				ne_detections.append(True)
		except AttributeError:
			ne_detections.append(False)

	#output = nltk.word_tokenize(word)
	#output = nltk.pos_tag(output)
	#output = nltk.ne_chunk(output)
	#print(output[0].label())
	
	# Exporting the data behaviours
	print("NOTICE: Data being exported to export/ne folder!")
	filename = "export/ne/export_"
	filename += str(time.time())
	filename += ".txt"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w") as file:
		for line in ne_detections:
			file.write(str(line))
			file.write("\n")

def main():
	data = collect_and_process.get_data()
	tr_items, tr_labels, te_items, te_labels = collect_and_process.collect_and_process(data)
	ne_detects = get_ne_tags(te_items)
	
if __name__ == "__main__":
    main()
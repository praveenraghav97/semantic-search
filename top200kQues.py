import json
import time
import sys
import csv


QUE_INDEXED = 200000

count = 0

f = open("top200KQuesData", 'w', encoding='latin1')


with open('./data/Questions.csv', encoding = 'latin1') as csvfile:

	readCSV = csv.reader(csvfile, delimiter=',')

	next(readCSV, None) # To skip Header

	for row in readCSV:

		doc_id = row[0]
		doc_title = row[5]

		f.write(doc_id + "," + doc_title + "\n")

		count += 1

		if count%200 == 0:
			print(count)

		if count == QUE_INDEXED:
			break

	print("Indexing Completed..")


	print("*"*50)

f.close()






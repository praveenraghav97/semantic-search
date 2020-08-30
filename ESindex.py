import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf
import tensorflow_hub as hub



'''This code connects ElasticSearch on localhost : 9200'''


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
	print("Connected to ES...")
else:
	print("Unable to connect")
	exit()


print("------------------------------------------------------------")


''' 
    In ES, index is same as DB in RDBMS. 
    Read each question and index into an "index" called "questions"

    Indexing only titles for this --to improve speed. In practice, its good to
    Index CONCATENATE(title+body)

    Define the index.


    --> Mapping: Structure of Index.
    --> Property/Field: name and type

 '''

idx_body = {"mappings" : {
		"properties": {
			"title": {
				"type": "text"
			},
			"title_vector": {
				"type": "dense_vector",
				"dims": 512
			}
		}}}

idx = es.indices.create(index='q-index', ignore=400, body=idx_body)
print(json.dumps(idx, indent=4))


print("---------------------------------------------------------------")


embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


QUESTIONS_INDEXED = 250000

# Columns are -- Id, OwnerUserId, CreationDate, ClosedDate, Score, Title, Body

cnt = 0

with open('./data/Questions.csv', encoding='latin1') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	next(readCSV, None) ### Skipping headers

	for row in readCSV:
		doc_id = row[0]
		title = row[5]
		vctr = tf.make_ndarray(tf.make_tensor_proto(embed([title]))).tolist()[0]
		
		bdy = {"title": title, "title_vector": vctr}

		rspns = es.index(index="q-index", id = doc_id, body = bdy)


		cnt += 1
		if cnt%100 == 0:
			print(cnt)
		if cnt == QUESTIONS_INDEXED:
			break

	print("Indexing Done...")


















































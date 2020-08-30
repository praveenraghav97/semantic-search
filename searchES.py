import json
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv
import tensorflow as tf 
import tensorflow_hub as hub


def connectES():
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

	if es.ping():
		print("Connection to ES is successfull")
	else:
		print("Unable to connect")
		sys.exit()

	print('*' * 50)
	return es


#Search by Keywords
def keywordSearch(es, q):
	b = {
		'query': {
			'match': {
				'title': q
			}
		}
	}

	res = es.search(index='q-index', body=b)
	print("Keyword Search: ")

	for hit in res['hits']['hits']:
		print(str(hit['_score']) + "\t" + hit['_source']['title'])


	print('*' * 50)

	return



#Search By Vector Simolarity
def sentenceSimilarityByNN(embed, es, sent):
	query_vector = tf.make_ndarray(tf.make_tensor_proto(embed([sent]))).tolist()[0]
	b = {
		'query': {
			'script_score': {
				'query': {
					'match_all': {}
				},
				'script': {
					'source': "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
					'params': { "query_vector": query_vector }
				}
			}
		}
	}

	res = es.search(index='q-index', body=b)

	print("Semantic Similarity Search")

	for hit in res['hits']['hits']:
		print(str(hit['_score']) + "\t" + hit['_source']['title'])

	print('*' * 50)


if __name__ == '__main__':

	es = connectES()
	embed = hub.load("./data/USE4")

	while(1):
		query = input("Enter a Query:  ")

		start = time.time()
		if query == 'END' or query=='end':
			break

		print("Query   : " + query)

		keywordSearch(es, query)

		sentenceSimilarityByNN(embed, es, query)

		end = time.time()

		print("Time Taken:  " + str( end - start))
		












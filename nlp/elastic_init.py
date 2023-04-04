import json
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

word_vectors = None

def init():
    global word_vectors
    word_vectors = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

def vectorize(question):
    return word_vectors.encode(question).tolist()

# Fill from fasttext, overwrites starting from index 0
def fillQAIndexFast(qa_file):

    es = Elasticsearch("http://localhost:9200")

    f = open(qa_file)
    data = json.load(f)
    
    index_ctr=0
    pair_count = len(data["qa-pairs"])
    with tqdm(total=pair_count) as pbar:
        for i in range(pair_count):
            for question in data["qa-pairs"][i]["question"]:

                q = {
                    "join": {
                        "name": "question",
                        "parent": str(index_ctr)
                    },
                    "body": question,
                    "vector": vectorize(question),
                    "index": i
                }
                #a = {
                #    "join": {
                #        "name": "answer",
                #    },
                #    "body": i["answer"][0],
                #    "vector": [0] * 768
                #}
                #es.index(index="question-answer", document=a, id=index_ctr)
                #index_ctr = index_ctr + 1
                es.index(index="question-answer", document=q, id=index_ctr, routing=True)
                index_ctr = index_ctr + 1

            pbar.update(1)

# Init elasticsearch, it will give an error when used twice since we need to delete index before using create() again
def initQAIndex():

    es = Elasticsearch("http://localhost:9200")
    
    mapping_properties = {
        "body": {
            "type": "text",
            "analyzer": "custom_turkish",
            "search_analyzer": "custom_turkish" #unless specified analyzer is used for both
        },
        "join": {
            "type": "join",
            "relations": {"answer": "question"}
        },
        "vector": {
            "type": "dense_vector",
            "dims": 768
        },
        "index": {
            "type": "integer"
        }
    }

    settings = {
        "analysis": {
            "filter": {
                "turkish_stop": {
                    "type":       "stop",
                    "stopwords":  "_turkish_" 
                },
                "turkish_lowercase": {
                    "type":       "lowercase",
                    "language":   "turkish"
                },
                "turkish_keywords": {
                    "type":       "keyword_marker",
                    "keywords":   ["örnek"] #check this 
                },
                "turkish_stemmer": {
                    "type":       "stemmer",
                    "language":   "turkish"
                }
            },
            "analyzer": {
                "custom_turkish": {
                    "tokenizer":  "standard",
                    "filter": [
                        "apostrophe",
                        "turkish_lowercase",
                        "turkish_stop",
                        "turkish_keywords",
                        "turkish_stemmer"
                    ]
                }
            }
        }
    }

    # To delete index: curl -X DELETE "localhost:9200/question-answer"
    es.indices.delete(index="question-answer", ignore_unavailable=True)
    es.indices.create(index="question-answer", settings=settings)
    es.indices.put_mapping(index="question-answer", properties=mapping_properties)

# We need to run this file to initialize Elasticsearch before sending requests
if __name__ == "__main__":
    init()
    initQAIndex()
    fillQAIndexFast("qa_pairs.json")
    print("ElasticSearch initialized.")
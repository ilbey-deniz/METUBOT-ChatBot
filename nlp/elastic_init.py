import json
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def initializeIndex(qa_file):
    word_vectors = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

    es = Elasticsearch("http://localhost:9200")

    f = open(qa_file)
    data = json.load(f)

    pair_count = len(data["qa-pairs"])

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
        "answer": {
            "type": "object",
            "enabled" : False
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
    
    with tqdm(total=pair_count) as pbar:
        for i in range(pair_count):
            a = {
                    "join": {
                        "name": "answer"
                    },
                    "answer": data["qa-pairs"][i]["answer"]
                }

            answer_id = es.index(index="question-answer", document=a, routing=True)["_id"]
            
            for question in data["qa-pairs"][i]["question"]:

                q = {
                    "join": {
                        "name": "question",
                        "parent": answer_id
                    },
                    "body": question,
                    "vector": word_vectors.encode(question).tolist()
                }

                es.index(index="question-answer", document=q, routing=True)

            pbar.update(1)

    print("ElasticSearch initialized.")

# We need to run this file to initialize Elasticsearch before sending requests
if __name__ == "__main__":
    initializeIndex("qa_pairs.json")
import json
from elasticsearch import Elasticsearch

# Converting these functions into a class may be a good idea

# Init elasticsearch, it will give an error when used twice since we need to delete index before using create() again
def initQAIndex():

    es = Elasticsearch("http://localhost:9200")
    
    mapping_properties = {
        "body": {
            "type": "text",
            "analyzer": "turkish",
            "search_analyzer": "turkish" #unless specified analyzer is used for both
        },
        "join": {
            "type": "join",
            "relations": {"answer": "question"}
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
                "rebuilt_turkish": {
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
    es.indices.create(index="question-answer", settings=settings)
    es.indices.put_mapping(index="question-answer", properties=mapping_properties)

# Fill from file, overwrites starting from index 0
def fillQAIndex(qa_file):

    es = Elasticsearch("http://localhost:9200")

    f = open(qa_file)
    data = json.load(f)
    
    index_ctr=0
    for i in data ["qa-pairs"]:
        q = {
            "join": {
                "name": "question",
                "parent": str(index_ctr)
            },
            "body": i["question"][0]
        }
        a = {
            "join": {
                "name": "answer",
            },
            "body": i["answer"][0]
        }
        es.index(index="question-answer", document=a, id=index_ctr)
        index_ctr = index_ctr + 1
        es.index(index="question-answer", document=q, id=index_ctr, routing=True)
        index_ctr = index_ctr + 1

# We will use this to get answer, I "guess" index 0 contains the max score result
def getResponse(question):

    es = Elasticsearch("http://localhost:9200")

    response = es.search(index="question-answer", query={
        "has_child": {
            "type": "question",
            "query": {
                "more_like_this": {
                    "fields": ["body"],
                    "like": question,
                    "min_term_freq": 1,
                    "min_doc_freq": 1,
                    "max_query_terms": 12
                }
            }
        }
    })

    if(len(response["hits"]["hits"]) > 0):
        return response["hits"]["hits"][0]["_source"]["body"]
    else:
        return "Hata"

# For test purposes, returns all together with results
def getSimiliarQuestion(question):

    es = Elasticsearch("http://localhost:9200")

    response = es.search(index="question-answer", query={
        "more_like_this": {
            "fields": ["body"],
            "like": question,
            "min_term_freq": 1,
            "min_doc_freq": 1,
            "max_query_terms": 12
        }
    })
    
    response_list = []
    for i in response["hits"]["hits"]:
        
        # There may be a better solution
        if i["_source"]["join"]["name"] == "question":
            response_list.append((i["_id"], i["_source"]["body"], i["_score"]))
    
    return response_list

# We need to run this file to initialize Elasticsearch before sending requests
if __name__ == "__main__":
    initQAIndex()
    fillQAIndex("qa_pairs.json")

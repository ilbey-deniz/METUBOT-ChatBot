import json
from elasticsearch import Elasticsearch
import ft

def initQAIndex():

    es = Elasticsearch("http://localhost:9200")
    
    mapping_properties = {
        "body": {
            "type": "text",
        },
        "body_vector": {
            "type": "dense_vector",
            "dims": 300
        },
        "tags": {
            "type": "keyword"
        },
        "join": {
            "type": "join",
            "relations": {"answer": "question"}
        }
    }

    # To delete index: curl -X DELETE "localhost:9200/question-answer"
    es.indices.create(index="question-answer")
    es.indices.put_mapping(index="question-answer", properties=mapping_properties)

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
            "body": i["question"][0],
            "body_vector": ft.embed(i["question"][0])
        }
        a = {   
            "join": {
                "name": "answer",
            },
            "body": i["answer"][0],
            "body_vector": ft.embed(i["answer"][0])
        }
        es.index(index="question-answer", document=a, id=index_ctr)
        index_ctr = index_ctr + 1
        es.index(index="question-answer", document=q, id=index_ctr, routing=True)
        index_ctr = index_ctr + 1

def getResponse(question):

    es = Elasticsearch("http://localhost:9200")

    # Search questions
    response = es.search(index="question-answer", query={
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'body_vector') + 1.0",
                "params": {"query_vector": ft.embed(question)}
            }
        }
    })
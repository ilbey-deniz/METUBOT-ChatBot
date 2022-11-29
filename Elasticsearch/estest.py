from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

answer = {
    "id" : 0,
    "text": "nasılsın",
    "my_join_field": {
        "name": "answer"
    }
}

question = {
    "id" : 1,
    "text": "iyiyim",
    "my_join_field": {
        "name": "question",
        "parent": "0"
    }
}

mapping = {
        "mappings": {
            "properties": {
                "my_join_field": {
                    "type": "join",
                    "relations": {
                        "answer": "question"
                    }
                }
            }
        }
}

resp = es.index(index="qna", id=0, document=answer)
print(resp['result'])

resp = es.index(index="qna", routing=1, id=1, document=question)
print(resp['result'])

resp = es.search(index="qna", query={"prefix": {"text" : "iyi" } }) #Find documents starting with prefix "iyi"

print("=========================================")
for hit in resp['hits']['hits']:
    print(hit['_source']['text'])

resp = es.search(index="qna", query={
    "has_parent": {
        "parent_type": "answer",
        "query": {
            "prefix": {"text" : "nası"} #Find documents whose parent (question) starts with "nası"
            }
        }
    })

print("=========================================")
for hit in resp['hits']['hits']:
    print(hit['_source']['text'])



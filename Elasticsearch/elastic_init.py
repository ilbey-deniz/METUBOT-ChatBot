import json
from elasticsearch import Elasticsearch

f = open("qa_pairs.json")
data = json.load(f)

mapping_properties = {
    "question": {"type": "text"},
    "answer": {"type": "text"},
    "join": {
        "type": "join",
        "relations": {"answer": "question"}
    }
}


es = Elasticsearch("http://localhost:9200")

#es.indices.create(index="question-answer")
es.indices.put_mapping(index="question-answer", properties=mapping_properties)

index_ctr=0
for i in data ["qa-pairs"]:
    q = {
        "join": {
            "name": "question",
            "parent": str(index_ctr)
        },
        "body": i["question"]
    }
    a = {
        "join": {
            "name": "answer",
        },
        "body": i["answer"]
    }
    es.index(index="question-answer", document=a, id=index_ctr)
    index_ctr = index_ctr + 1
    es.index(index="question-answer", document=q, id=index_ctr, routing=True)
    index_ctr = index_ctr + 1

def getResponse(question):
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

#print(getResponse("horde istiyom"))

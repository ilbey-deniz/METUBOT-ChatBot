import json
import nlp.fast as fast
from elasticsearch import Elasticsearch

# Converting these functions into a class may be a good idea

data = None

# Get answer based on text similiarity
def getTextResponse(question):

    es = Elasticsearch("http://localhost:9200")

    # Search questions
    response = es.search(index="question-answer", query={
        "more_like_this": {
            "fields": ["body"],
            "like": question,
            "analyzer": "custom_turkish",
            "min_term_freq": 1,
            "min_doc_freq": 1,
            "max_query_terms": 12
        }
    })

    print(response)

    if len(response["hits"]["hits"]) > 0:
        temp = response["hits"]["hits"][0]["_source"]

        if temp["join"]["name"] == "question":
            answer_resp = es.search(index="question-answer", query={
                "has_child": {
                    "type": "question",
                    "query": {
                        "ids": {
                            "values": [response["hits"]["hits"][0]["_id"]]
                        }
                    }
                }
            })

            temp = answer_resp["hits"]["hits"][0]["_source"]
        
        return temp["body"]
    else:
        # No hit
        return "Üzgünüm, ne sormak istediğinizi anlayamadım."
    
# Get answer based on vector similiarity
def getVectorResponse(question):

    es = Elasticsearch("http://localhost:9200")

    response = es.search(index="question-answer", query={
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                "params": {"query_vector": fast.vectorize(question)}
            }
        }
    })

    print(response)

    if len(response["hits"]["hits"]) > 0:
        temp = response["hits"]["hits"][0]["_source"]

        #if temp["join"]["name"] == "question":
        #    answer_resp = es.search(index="question-answer", query={
        #        "has_child": {
        #            "type": "question",
        #            "query": {
        #                "ids": {
        #                    "values": [response["hits"]["hits"][0]["_id"]]
        #                }
        #            }
        #        }
        #    })
#
        #    temp = answer_resp["hits"]["hits"][0]["_source"]
        #
        val = data["qa-pairs"][temp["index"]]["answer"]
        
        if type(val[0]==str):
            return val[0]
        else:
            return val
    else:
        # No hit
        return "Üzgünüm, ne sormak istediğinizi anlayamadım."

# Not up-to-date
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

def init():
    global data

    f = open("nlp/qa_pairs.json")
    data = json.load(f)
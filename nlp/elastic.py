import json
import nlp.fast as fast
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from Answerer import Answerer

class ElasticsearchInterface(Answerer):
    def __init__(self, answerGenerator=None) -> None:
        super().__init__(answerGenerator)

        self.st = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

        self.es = Elasticsearch("http://localhost:9200")

        f = open("nlp/qa_pairs.json")
        self.data = json.load(f)

    def vectorize(self, question):
        return self.st.encode(question).tolist()
    
    def answer(self, question):
        return self.getResponse(question)
    
    # Get answer based on vector similiarity
    def getResponse(self, question):
        question_response = self.es.search(index="question-answer", query={
            "script_score": {
                "query": {
                    "multi_match": {
                        "query": "question",
                        "fields": ["join"]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": self.vectorize(question)}
                }
            }
        })

        if len(question_response["hits"]["hits"]) > 0:
            answer_response = self.es.get(index="question-answer", id=question_response["hits"]["hits"][0]["_source"]["join"]["parent"])
            result = answer_response["_source"]["answer"]

            print(f'Most similiar question: {question_response["hits"]["hits"][0]["_source"]["body"]}')
            print(f'Similiarity: {question_response["hits"]["max_score"]}')
            print(f'Parent id: {question_response["hits"]["hits"][0]["_source"]["join"]["parent"]}')
            print(f'Answer: {result}')

            if question_response["hits"]["max_score"] < 1.36: #Not final
                # Similiarity check
                return "Üzgünüm, ne sormak istediğinizi anlayamadım."

            if isinstance(result[0], str):
                return result[0]
            else:
                return result
            
            #if type(result[0]==str):
            #    return result[0]
            #else:
            #    return result
        else:
            # No hit
            return "Üzgünüm, ne sormak istediğinizi anlayamadım."
        
    def addQuestion(self, question, answer):
        a = {
                    "join": {
                        "name": "answer"
                    },
                    "answer": [answer]
                }

        answer_id = self.es.index(index="question-answer", document=a, routing=True)["_id"]
        
        q = {
                    "join": {
                        "name": "question",
                        "parent": answer_id
                    },
                    "body": question,
                    "vector": self.vectorize(question)
                }

        self.es.index(index="question-answer", document=q, routing=True)

    # Returns a list of q-a pairs in the same format as qa_pairs.json
    def getPage(self, from_, size):
        result = []

        response = self.es.search(index="question-answer", from_=from_, size=size, query={
            "multi_match": {
                "query": "answer",
                "fields": ["join"]
            }
        })

        for res in response["hits"]["hits"]:

            ques = self.es.search(index="question-answer", query={
                "parent_id":{
                    "type": "question",
                    "id": res["_id"]
                }
            })

            result.append({"question": [q["_source"]["body"] for q in ques["hits"]["hits"]],
                           "answer": res["_source"]["answer"],
                           "category": res["_source"]["category"]})
            
        return result


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
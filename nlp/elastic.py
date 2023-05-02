import json
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

    def vectorize(self, question: str):
        return self.st.encode(question).tolist()
    
    def answer(self, question: str):
        return self.getResponse(question)
    
    # Get answer based on vector similiarity
    def getResponse(self, question: str):
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

        else:
            # No hit
            return "Üzgünüm, ne sormak istediğinizi anlayamadım."
        
    def addQuestion(self, questions: list, answer: list, category: str) -> None:
        a = {
                "join": {
                    "name": "answer"
                },
                "answer": answer,
                "category": category
            }

        answer_id = self.es.index(index="question-answer", document=a, routing=True)["_id"]
        
        for question in questions:
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
    def getPage(self, from_: int, size: int) -> list:
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
    
    # Deletes answer document and all questions related to it
    def deleteAnswer(self, id: str) -> None:
        ques = self.es.search(index="question-answer", query={
            "parent_id":{
                "type": "question",
                "id": id #Find documents whose parent (question) starts with "nası"
            }
        })
        
        for q in ques["hits"]["hits"]:
            self.es.delete(index="question-answer", id=q["_id"])

            self.es.delete(index="question-answer", id=id)

    # Deletes a single question document
    def deleteQuestion(self, id: str) -> None:
        self.es.delete(index="question-answer", id=id)

    # Updates answer document and all questions related to it
    # Basicially delete and add
    def updateAnswer(self, id: str, questions: list, answer: list, category: str) -> None:
        self.deleteAnswer(id)
        self.addQuestion(questions, answer, category)

    # Updates question without touching answer
    def updateQuestion(self, id: str, question: str) -> None:
        answer_id = self.es.get(index="question-answer", id=id)["_source"]["join"]["parent"]

        self.deleteQuestion(id)

        q = {
            "join": {
                "name": "question",
                "parent": answer_id
            },
            "body": question,
            "vector": self.vectorize(question)
        }

        self.es.index(index="question-answer", document=q, id=id, routing=True)

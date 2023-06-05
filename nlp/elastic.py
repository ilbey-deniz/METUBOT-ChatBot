import json
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from Answerer import Answerer, Answer


class ElasticsearchInterface(Answerer):
    def __init__(self, answerGenerator=None) -> None:
        super().__init__(answerGenerator)

        self.st = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

        self.es = Elasticsearch("http://localhost:9200")

        f = open("nlp/qa_pairs.json")
        self.data = json.load(f)

    def vectorize(self, question: str):
        return self.st.encode(question).tolist()

    def answer(self, question: str) -> Answer:
        return self.getResponse(question)

    # Get answer based on vector similiarity
    def getResponse(self, question: str) -> Answer:
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
        response = Answer({"answer": ["Üzgünüm, ne sormak istediğinizi anlayamadım."], "buttons": []}, 1, "Cevabı Meçhul")

        if len(question_response["hits"]["hits"]) > 0:
            answer_response = self.es.get(index="question-answer", id=question_response["hits"]["hits"][0]["_source"]["join"]["parent"])
            result = {"question":question_response["hits"]["hits"][0]["_source"]["body"], "answer": answer_response["_source"]["answer"], "buttons": answer_response["_source"]["buttons"] }
            category = answer_response["_source"]["category"]
            response.similarity = question_response["hits"]["max_score"] -1

            print(f'Most similiar question: {question_response["hits"]["hits"][0]["_source"]["body"]}')
            print(f'Similiarity: {response.similarity}')
            print(f'Parent id: {question_response["hits"]["hits"][0]["_source"]["join"]["parent"]}')
            print(f'Answer: {result}')

            if response.similarity < 0.36: #Not final
                response.text["question"] = question_response["hits"]["hits"][0]["_source"]["body"]
                return response

            response.category = category

            #if isinstance(result[0], str):
            #    response.text = result[0]
            #else:
            #    response.text = result

            response.text = result

            return response

        else:
            # No hit
            return response

    def addQuestion(self, questions: list, answer: list, category: str, buttons: list) -> str:
        a = {
                "join": {
                    "name": "answer"
                },
                "answer": answer,
                "category": category,
                "buttons": buttons
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

        return answer_id

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

            result.append({"id": res["_id"],
                           "questions": [q["_source"]["body"] for q in ques["hits"]["hits"]],
                           "answers": res["_source"]["answer"],
                           "category": res["_source"]["category"],
                           "buttons": res["_source"]["buttons"]})

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

    # Deletes a single question document. TODO: Unecessary
    def deleteQuestion(self, id: str) -> None:
        self.es.delete(index="question-answer", id=id)

    # Updates answer document and all questions related to it
    # Basicially delete and add
    def updateAnswer(self, id: str, questions: list, answer: list, category: str, buttons: list) -> str:
        self.deleteAnswer(id)
        return self.addQuestion(questions, answer, category, buttons)

    # Updates question without touching answer TODO: Unecessary
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

    def initFromDict(self, data: dict) -> None:
        pair_count = len(data["qa-pairs"])

        for i in range(pair_count):
            a = {
                    "join": {
                        "name": "answer"
                    },
                    "answer": data["qa-pairs"][i]["answer"],
                    "category": data["qa-pairs"][i]["category"],
                    "buttons": data["qa-pairs"][i]["buttons"]
                }

            answer_id = self.es.index(index="question-answer", document=a, routing=True)["_id"]
            
            for question in data["qa-pairs"][i]["question"]:

                q = {
                    "join": {
                        "name": "question",
                        "parent": answer_id
                    },
                    "body": question,
                    "vector": self.st.encode(question).tolist()
                }

                self.es.index(index="question-answer", document=q, routing=True)
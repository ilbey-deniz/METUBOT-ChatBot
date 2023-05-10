from timeit import default_timer as timer
from datetime import timedelta
from elasticsearch import Elasticsearch
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

es = Elasticsearch('http://localhost:9200')
st = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

def vectorize(question: str):
        return st.encode(question).tolist()

def getTestResponse(question: str):
        question_response = es.search(index="question-answer", query={
            "script_score": {
                "query": {
                    "multi_match": {
                        "query": "question",
                        "fields": ["join"]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": vectorize(question)}
                }
            }
        })

        if len(question_response["hits"]["hits"]) > 0:
            answer_response = es.get(index="question-answer", id=question_response["hits"]["hits"][0]["_source"]["join"]["parent"])
            result = answer_response["_source"]["answer"]

            if question_response["hits"]["max_score"] < 1.36: #Not final
                # Similiarity check
                return "Üzgünüm, ne sormak istediğinizi anlayamadım."

            return result

        else:
            # No hit
            return "Üzgünüm, ne sormak istediğinizi anlayamadım."
        
with open("elastic_test_input.json", "r") as f:
    with open("elastic_test_results.txt", "w") as out:
        testinput = json.load(f)
        testcases = 0
        successcount = 0
        timer_start = False

        for pair in testinput["qa-pairs"]:
            testcases += len(pair["question"])

        with tqdm(total=testcases) as pbar:
            for pair in testinput["qa-pairs"]:
                for question in pair["question"]:
                    response = getTestResponse(question)
                    if response == pair["answer"]:
                        successcount += 1
                    else:
                        log = f"""
Question: {pair["question"]}
Result: {response}
Expected: {pair["answer"]}
"""

                        out.write(log)

                    pbar.update(1)

                    if not timer_start:
                        start = timer()
                        timer_start = True

        end = timer()

        print(f"Test completed in {timedelta(seconds=end-start)}. Transformer initialization time not included.")
        print("See elastic_test_results.txt for results.")
        print(f"Success rate: {successcount/testcases}")
import requests

URL = "http://localhost:8080/ask"

# Each line in question.txt is a question
with open('questions.txt', 'r') as f:
    for question in f:
        if question[-1] == '\n':
            question = question[:-1]
        PARAMS = {'question': question}
        response = requests.get(url=URL, params=PARAMS)
        print("==========================================")
        print(question)
        print("")
        print(response.content.decode(encoding='utf-8'))
from flask import Flask, jsonify, request
from ElasticAnswerer import ElasticAnswerer
from FasttextAnswerer import FasttextAnswerer
app = Flask(__name__)

@app.route('/ask')
def get_incomes():
    elastic_answerer = ElasticAnswerer()
    return elastic_answerer.answer(request.args.get('question'))

if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with get request to /ask?question=your_question")
    app.run(host="0.0.0.0", port="8080", debug=False)

from flask import Flask, jsonify, request
from ElasticAnswerer import ElasticAnswerer
from FasttextAnswerer import FasttextAnswerer
from AnswerGeneratorMetu import AnswerGeneratorMetu
app = Flask(__name__)

answer_generator = AnswerGeneratorMetu()
elastic_answerer = ElasticAnswerer(answer_generator)
fasttext_answerer = FasttextAnswerer(answer_generator)

@app.route('/ask')
def get_incomes():
    return elastic_answerer.answer(request.args.get('question'))

@app.route('/askFast')
def get_incomes_fast():
    return fasttext_answerer.answer(request.args.get('question'))

if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with get request to /ask?question=your_question")
    app.run(host="0.0.0.0", port="8080", debug=False)
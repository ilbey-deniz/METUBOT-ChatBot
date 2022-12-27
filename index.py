from flask import Flask, jsonify, request
from ElasticAnswerer import ElasticAnswerer
from FasttextAnswerer import FasttextAnswerer
from AnswerGeneratorMetu import AnswerGeneratorMetu
from data.metu.json_qapairs_manager import add_questions_manually

app = Flask(__name__)

answer_generator = AnswerGeneratorMetu()
elastic_answerer = ElasticAnswerer(answer_generator)
fasttext_answerer = FasttextAnswerer(answer_generator)

@app.route('/ask')
def get_incomes():
    return elastic_answerer.generatedAnswer(request.args.get('question'))

@app.route('/askFast')
def get_incomes_fast():
    return fasttext_answerer.generatedAnswer(request.args.get('question'))

@app.route('/addQuestion')
def add_questions():
    category = request.args.get("category")
    question = request.args.get("question")
    answer = request.args.get("answer")
    add_questions_manually(category=category, questions=[question], answers=[answer])
    return "No error"

@app.route('/reportQuestion')
def report_questions():
    question = request.args.get("question")
    answer = request.args.get("answer")
    created_at = request.args.get("created_at")

    print(question)
    print(answer)
    print(created_at)
    return "No error"

if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with get request to /ask?question=your_question")
    app.run(host="0.0.0.0", port="8080", debug=False)
from Answerer import Answerer
import nlp.elastic_init as elastic


class ElasticAnswerer(Answerer):
    def __init__(self, answerGenerator=None):
        super().__init__(answerGenerator)

    def answer(self, question):
        return elastic.getResponse(question)

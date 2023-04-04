from Answerer import Answerer
import nlp.elastic as elastic
import nlp.fast as fast


class ElasticAnswerer(Answerer):
    def __init__(self, answerGenerator=None):
        super().__init__(answerGenerator)
        fast.init()
        elastic.init()

    def answer(self, question):
        return elastic.getVectorResponse(question)

from Answerer import Answerer
import nlp.elastic_init as elastic
import nlp.fast as fast


class ElasticAnswerer(Answerer):
    def __init__(self, answerGenerator=None):
        super().__init__(answerGenerator)
        fast.init()
        elastic.initQAIndex()
        #elastic.fillQAIndexFast("nlp/qa_pairs.json")

    def answer(self, question):
        return elastic.getResponse(question)

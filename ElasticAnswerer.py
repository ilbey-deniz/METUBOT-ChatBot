from Answerer import Answerer
import Elasticsearch.elastic_init as elastic

class ElasticAnswerer(Answerer):
    def answer(self, question):
        return elastic.getResponse(question)

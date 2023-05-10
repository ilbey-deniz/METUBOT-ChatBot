from Answerer import Answerer, Answer


class DummyAnswerer(Answerer):
    def __init__(self, answerGenerator=None):
        super().__init__(answerGenerator)
        #elastic.fillQAIndexFast("nlp/qa_pairs.json")

    def answer(self, question):
        return Answer("Size daha iyi hizmet verebilmek için calisiyoruz. ^_^", 1, "Dummy")
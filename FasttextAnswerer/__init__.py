from Answerer import Answerer
import nlp.fast as fast
import fasttext

MODEL_DIR = r"./backend/cc.tr.300.bin"


class FasttextAnswerer(Answerer):
    def __init__(self, answerGenerator=None):
        super().__init__(answerGenerator)
        self.ft = fasttext.load_model(MODEL_DIR)
        #fasttext.util.reduce_model(self.ft, 100)

    def answer(self, question):
        return fast.NEWgetAnswer(self.ft, question)

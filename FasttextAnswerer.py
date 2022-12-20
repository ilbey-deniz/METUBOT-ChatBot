from Answerer import Answerer
import nlp.fasttext.fasttext as myFasttext
import fasttext

MODEL_DIR = r"/home/metubot/metubot/backend/cc.tr.300.bin"

class FasttextAnswerer(Answerer):

    def __init__(self):
        self.ft = fasttext.load_model(MODEL_DIR)

    def answer(self, question):
        return myFasttext.getAnswer(self.ft, question)
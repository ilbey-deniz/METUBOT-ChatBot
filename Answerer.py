class Answerer:
    def __init__(self, answerGenerator = None):
        self.answerGenerator = answerGenerator
        # This is dict of keywords to generate dynamic answers.


    def answer(self, question):
        return 'Override me in a subclass!'

    def generatedAnswer(self, question):
        if self.answerGenerator is None:
            return self.answer(question)
        else:
            return self.answerGenerator.generateAnswer(self.answer(question))

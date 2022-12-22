from AnswerGenerator import AnswerGenerator

class AnswerGenerator:
    def __init__(self):
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations = {}

    def generateAnswer(self, answer):
        for keyword in self.answerGenerations:
            if keyword in answer:
                generated = self.answerGenerations[keyword]()
                answer = answer.replace(keyword, generated)
        return answer

from Answerer import Answer


class AnswerGenerator:
    def __init__(self):
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations = {}

    def generate(self, answer: Answer) -> Answer:
        for keyword in self.answerGenerations:
            if keyword in answer.text:
                generated = self.answerGenerations[keyword]()
                answer.text = answer.text.replace(keyword, generated)
        return answer

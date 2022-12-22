from AnswerGenerator import AnswerGenerator


class AnswerGeneratorMetu(AnswerGenerator):
    def __init__(self):
        super().__init__()
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations['GET_METU_FOOD'] = self.getMetuFood
        self.answerGenerations['GET_TODAYS_DATE'] = self.getTodaysDate
        # new answerGenerations can be added here

    # todo: implement this
    def getMetuFood(self):
        return 'Metu food'

    # todo: implement this
    def getTodaysDate(self):
        return 'Todays date'

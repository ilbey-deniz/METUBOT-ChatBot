from AnswerGenerator import AnswerGenerator
import data.metu.catering.cafeteria as cf
import data.metu.departments.ceng as ceng


class AnswerGeneratorMetu(AnswerGenerator):
    def __init__(self):
        super().__init__()
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations['GET_METU_FOOD'] = self.getMetuFood
        self.answerGenerations['GET_TODAYS_DATE'] = self.getTodaysDate
        self.answerGenerations['GET_CENG_CURRICULUM'] = self.getCengCurriculum
        # new answerGenerations can be added here

    # todo: implement this
    def getMetuFood(self):
        return cf.yemek()

    # todo: implement this
    def getTodaysDate(self):
        return 'Todays date'

    def getCengCurriculum(self):
        return ceng.curriculum()


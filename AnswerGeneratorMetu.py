from AnswerGenerator import AnswerGenerator
import data.metu.scraping as sc


class AnswerGeneratorMetu(AnswerGenerator):
    def __init__(self):
        super().__init__()
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations['GET_METU_FOOD'] = self.getMetuFood
        self.answerGenerations['GET_TODAYS_DATE'] = self.getTodaysDate
        self.answerGenerations['GET_CENG_CURRICULUM'] = self.getCengCurriculum
        self.answerGenerations['GET_RING_TIMES'] = self.getRingTimes
        self.answerGenerations['GET_CALENDAR'] = self.getCalendar
        self.answerGenerations['GET_CAFETERIA_TIMES'] = self.getCafeteriaTimes
        self.answerGenerations['GET_CAFETERIA_PRICE'] = self.getCafeteriaPrice

        # new answerGenerations can be added here

    def getMetuFood(self):
        return sc.yemek()

    def getTodaysDate(self):
        return sc.saat()

    def getCengCurriculum(self):
        return sc.cengcurriculum()

    def getRingTimes(self):
        return sc.ring_saatleri()

    def getCalendar(self):
        return sc.takvim()

    def getCafeteriaTimes(self):
        return sc.saatler()

    def getCafeteriaPrice(self): #TODO: It has a a parameter.
        return sc.fiyat()
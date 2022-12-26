from AnswerGenerator import AnswerGenerator
import data.metu.catering.cafeteria as cf
import data.metu.departments.ceng as ceng
import data.metu.time.time as time
import data.metu.teleportation.rings as ring


class AnswerGeneratorMetu(AnswerGenerator):
    def __init__(self):
        super().__init__()
        # This is dict of keywords to generate dynamic answers.
        self.answerGenerations['GET_METU_FOOD'] = self.getMetuFood
        self.answerGenerations['GET_TODAYS_DATE'] = self.getTodaysDate
        self.answerGenerations['GET_CENG_CURRICULUM'] = self.getCengCurriculum
        self.answerGenerations['GET_RING_TIMES'] = self.getRingTimes
        self.answerGenerations['GET_CALENDAR'] = self.getCalendar
        # new answerGenerations can be added here

    def getMetuFood(self):
        return cf.yemek()

    def getTodaysDate(self):
        return time.saat()

    def getCengCurriculum(self):
        return ceng.curriculum()

    def getRingTimes(self):
        return ring.ring_saatleri()

    def getCalendar(self):
        return time.takvim()

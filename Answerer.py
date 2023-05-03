from abc import ABC, abstractmethod
from dataclasses import dataclass


class Answerer(ABC):
    def __init__(self, answerGenerator = None):
        self.answerGenerator = answerGenerator
        # This is dict of keywords to generate dynamic answers.

    @abstractmethod
    def answer(self, question) -> 'Answer':
        pass

    def generatedAnswer(self, question) -> 'Answer':
        if self.answerGenerator is None:
            return self.answer(question)
        else:
            return self.answerGenerator.generate(self.answer(question))


@dataclass
class Answer:
    text: str
    similarity: float
    category: str

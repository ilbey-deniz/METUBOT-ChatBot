from sqlalchemy.orm import declarative_base
from sqlalchemy import *

# create a declarative base
Base = declarative_base()

# The ORM class to represent question_table for questions added by user from the front-end.
class Questions(Base):
    __tablename__ = "main_questions"

    Qid = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(512))
    category = Column(String(60))
    count = Column(Integer)


# The ORM class to represent user_feedback for reported questions coming from the front-end.
class Feedbacks(Base):
    __tablename__ = "user_feedbacks"

    Fid = Column(Integer, primary_key=True)
    asked_question = Column(String(255))
    is_liked = Column(BOOLEAN)
    report_message = Column(String(255))
    similarity = Column(FLOAT)
    # created_at = Column(DateTime)
    # category = Column(String(60))
    # count = Column(Integer)


# The ORM class to represent feedback_activity to create relation question with report.
class Feedback_activity(Base):
    __tablename__ = "feedback_activity"

    Qid = Column(Integer, ForeignKey("main_questions.Qid"), primary_key=True, nullable=False)
    Fid = Column(Integer, ForeignKey("user_feedbacks.Fid"), primary_key=True, nullable=False)
    created_at = Column(DateTime)

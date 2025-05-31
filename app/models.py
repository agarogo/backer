from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String)
    test1_percentage = Column(Float, nullable=True)
    test2_percentage = Column(Float, nullable=True)
    test3_percentage = Column(Float, nullable=True)
    test4_percentage = Column(Float, nullable=True)

    quiz_results = relationship("QuizResult", back_populates="user")

class Question(Base):
    __tablename__ = "Questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    correct_answer = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)
    total_questions = Column(Integer)
    test_percentage = Column(Float)
    incorrect_questions = Column(JSON)
    test_type = Column(Integer)

    user = relationship("User", back_populates="quiz_results")

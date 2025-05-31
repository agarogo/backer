from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

# ----- USER -----
class UserBase(BaseModel):
    nickname: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    test1_percentage: Optional[float] = None
    test2_percentage: Optional[float] = None
    test3_percentage: Optional[float] = None
    test4_percentage: Optional[float] = None

    class Config:
        from_attributes = True

# ----- QUESTION -----
class QuestionBase(BaseModel):
    question_text: str
    correct_answer: str
    option1: str
    option2: str
    option3: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True

# ----- QUIZ RESULT -----
class QuizResultCreate(BaseModel):
    score: int
    total_questions: int
    test_percentage: float
    incorrect_questions: List[int]
    test_type: int

class QuizResult(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    score: int
    total_questions: int
    test_percentage: float
    incorrect_questions: List[int]
    test_type: int

    class Config:
        from_attributes = True

# ----- QUIZ SUBMISSION -----
class QuizSubmission(BaseModel):
    answers: Dict[str, str]
    test_type: int
    skip: int
    limit: int
class UserRating(BaseModel):
    nickname: str
    avg_percentage: float

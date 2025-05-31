from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        nickname=user.nickname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_test_percentage(db: Session, user_id: int, test_type: int, test_percentage: float):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if test_type == 1:
            db_user.test1_percentage = test_percentage
        elif test_type == 2:
            db_user.test2_percentage = test_percentage
        elif test_type == 3:
            db_user.test3_percentage = test_percentage
        elif test_type == 4:
            db_user.test4_percentage = test_percentage
        db.commit()
        db.refresh(db_user)
    return db_user

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()

def create_quiz_result(db: Session, result: schemas.QuizResultCreate, user_id: int):
    db_result = models.QuizResult(
        user_id=user_id,
        score=result.score,
        total_questions=result.total_questions,
        test_percentage=result.test_percentage,
        incorrect_questions=result.incorrect_questions,
        test_type=result.test_type
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    update_user_test_percentage(db, user_id, result.test_type, result.test_percentage)
    return db_result

def get_user_results(db: Session, user_id: int):
    return db.query(models.QuizResult).filter(models.QuizResult.user_id == user_id).all()

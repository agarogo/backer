from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.get("/questions/")
def get_questions(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    return db.query(models.Question).offset(skip).limit(limit).all()

@router.post("/submit/", response_model=schemas.QuizResult)
def submit_quiz(
    submission: schemas.QuizSubmission,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    questions = db.query(models.Question).offset(submission.skip).limit(submission.limit).all()

    if not questions:
        raise HTTPException(status_code=404, detail="Вопросы не найдены")

    correct_count = 0
    incorrect_ids = []

    for question in questions:
        user_answer = submission.answers.get(str(question.id))
        if user_answer == question.correct_answer:
            correct_count += 1
        else:
            incorrect_ids.append(question.id)

    percentage = round((correct_count / len(questions)) * 100, 2)

    if submission.test_type == 1:
        current_user.test1_percentage = percentage
    elif submission.test_type == 2:
        current_user.test2_percentage = percentage
    elif submission.test_type == 3:
        current_user.test3_percentage = percentage
    elif submission.test_type == 4:
        current_user.test4_percentage = percentage

    db.commit()

    return schemas.QuizResult(
        score=correct_count,
        total_questions=len(questions),
        test_percentage=percentage,
        incorrect_questions=incorrect_ids
    )

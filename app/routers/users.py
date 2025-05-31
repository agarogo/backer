from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, dependencies
from ..database import get_db
from app import models
from app.routers.auth import get_password_hash  # 👈 добавлено

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)  # 👈 исправлено
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: schemas.User = Depends(dependencies.get_current_user)):
    return current_user

@router.patch("/{user_id}/test{test_num}/", response_model=schemas.User)
def update_test_result(
    user_id: int,
    test_num: int,
    percentage: float,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user)
):
    if test_num not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Test number must be 1-4")
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return crud.update_user_test_percentage(db=db, user_id=user_id, test_type=test_num, test_percentage=percentage)

@router.get("/rating", response_model=List[schemas.UserRating])
def get_user_ratings(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    ratings = []

    for user in users:
        percentages = [
            p for p in [
                user.test1_percentage,
                user.test2_percentage,
                user.test3_percentage,
                user.test4_percentage,
            ] if p is not None
        ]
        if percentages:
            avg = sum(percentages) / len(percentages)
            ratings.append({
                "nickname": user.nickname,
                "avg_percentage": round(avg, 2)
            })

    ratings.sort(key=lambda x: x["avg_percentage"], reverse=True)
    return ratings

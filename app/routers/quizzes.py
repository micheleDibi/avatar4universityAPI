from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lesson, Quiz, QuizQuestion
from app.schemas.schemas import QuizList, QuizDetail, QuizQuestionList, QuizQuestionDetail

router = APIRouter(tags=["quizzes"])


@router.get("/lessons/{lesson_id}/quizzes", response_model=List[QuizList])
def list_lesson_quizzes(
    lesson_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return (
        db.query(Quiz)
        .filter(Quiz.lesson_id == lesson_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/quizzes/{quiz_id}", response_model=QuizDetail)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.get("/quizzes/{quiz_id}/questions", response_model=List[QuizQuestionList])
def list_quiz_questions(
    quiz_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return (
        db.query(QuizQuestion)
        .filter(QuizQuestion.quiz_id == quiz_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/questions/{question_id}", response_model=QuizQuestionDetail)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

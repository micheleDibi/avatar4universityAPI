from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.models import Lesson, Quiz, QuizQuestion, Module, Course
from app.schemas.schemas import QuizList, QuizDetail, QuizQuestionList, QuizQuestionDetail

router = APIRouter(tags=["quizzes"])


def _verify_lesson_in_org(db: Session, lesson_id: int, org_id: int) -> Lesson:
    lesson = (
        db.query(Lesson)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .filter(Lesson.id == lesson_id, Course.organization_id == org_id)
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


def _get_quiz_in_org(db: Session, quiz_id: int, org_id: int) -> Quiz:
    quiz = (
        db.query(Quiz)
        .join(Lesson, Lesson.id == Quiz.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .filter(Quiz.id == quiz_id, Course.organization_id == org_id)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.get("/lessons/{lesson_id}/quizzes", response_model=List[QuizList])
def list_lesson_quizzes(
    lesson_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    _verify_lesson_in_org(db, lesson_id, org_id)
    return (
        db.query(Quiz)
        .filter(Quiz.lesson_id == lesson_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/quizzes/{quiz_id}", response_model=QuizDetail)
def get_quiz(
    quiz_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return _get_quiz_in_org(db, quiz_id, org_id)


@router.get("/quizzes/{quiz_id}/questions", response_model=List[QuizQuestionList])
def list_quiz_questions(
    quiz_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    _get_quiz_in_org(db, quiz_id, org_id)
    return (
        db.query(QuizQuestion)
        .filter(QuizQuestion.quiz_id == quiz_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/questions/{question_id}", response_model=QuizQuestionDetail)
def get_question(
    question_id: int,
    org_id: int = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    question = (
        db.query(QuizQuestion)
        .join(Quiz, Quiz.id == QuizQuestion.quiz_id)
        .join(Lesson, Lesson.id == Quiz.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .join(Course, Course.id == Module.course_id)
        .filter(QuizQuestion.id == question_id, Course.organization_id == org_id)
        .first()
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

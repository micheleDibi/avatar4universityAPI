from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# --- Slide ---

class SlideSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    section_id: int
    title: str
    type: str
    contents_json: Optional[str] = None


# --- Section ---

class SectionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    title: Optional[str] = None
    content: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: Optional[int] = None
    audio_url: Optional[str] = None
    audio_duration: Optional[float] = None
    raw_video_url: Optional[str] = None
    avatar_video_url: Optional[str] = None
    cloned_audio_url: Optional[str] = None
    slides_and_avatar_video_url: Optional[str] = None
    slide_audio_video_url: Optional[str] = None
    section_pdf_url: Optional[str] = None
    lesson_id: Optional[int] = None


class SectionList(SectionBase):
    pass


class SectionDetail(SectionBase):
    slide: Optional[SlideSchema] = None


# --- Open Question ---

class OpenQuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    lesson_id: Optional[int] = None


# --- Quiz Option ---

class QuizOptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    option_text: str
    is_correct: bool
    quiz_question_id: Optional[int] = None


# --- Quiz Question ---

class QuizQuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    difficulty: str
    origin_lesson: Optional[int] = None
    quiz_id: Optional[int] = None


class QuizQuestionList(QuizQuestionBase):
    pass


class QuizQuestionDetail(QuizQuestionBase):
    options: list[QuizOptionSchema] = []


# --- Quiz ---

class QuizBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    lesson_id: Optional[int] = None


class QuizList(QuizBase):
    pass


class QuizDetail(QuizBase):
    questions: list[QuizQuestionList] = []


# --- Lesson ---

class LessonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    objectives_json: Optional[str] = None
    mandatory_topics_json: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: Optional[int] = None
    avatar_video_url: Optional[str] = None
    mp4_video_url: Optional[str] = None
    slides_pdf_url: Optional[str] = None
    slides_and_avatar_video_url: Optional[str] = None
    slides_and_audio_video_url: Optional[str] = None
    lesson_type: Optional[str] = None
    module_id: Optional[int] = None


class LessonList(LessonBase):
    pass


class LessonDetail(LessonBase):
    sections: list[SectionList] = []
    open_questions: list[OpenQuestionSchema] = []
    quizzes: list[QuizList] = []


# --- Module ---

class ModuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    duration_minutes: Optional[int] = None
    order: Optional[int] = None
    course_id: Optional[int] = None


class ModuleList(ModuleBase):
    pass


class ModuleDetail(ModuleBase):
    lessons: list[LessonList] = []


# --- Course ---

class CourseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    title: Optional[str] = None
    language: Optional[str] = None
    duration_minutes: Optional[int] = None
    banner_image_url: Optional[str] = None
    slides_url: Optional[str] = None
    slides_pdf_url: Optional[str] = None
    course_type: str
    created_at: datetime
    updated_at: datetime
    is_draft: Optional[bool] = None
    modules_count: Optional[int] = None


class CourseList(CourseBase):
    pass


class CourseDetail(CourseBase):
    modules: list[ModuleList] = []

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    slide_template_id = Column(Integer)
    name = Column(String, nullable=False)
    title = Column(String)
    language = Column(String)
    prompt = Column(String)
    slides_configuration = Column(String)
    duration_minutes = Column(Integer)
    banner_image_url = Column(String)
    slides_url = Column(String)
    avatar_id = Column(Integer)
    modules_structure_json = Column(String)
    slides_pdf_url = Column(String)
    creator_user_id = Column(Integer)
    organization_id = Column(Integer)
    course_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_draft = Column(Boolean)
    modules_count = Column(Integer, default=0)

    modules = relationship("Module", back_populates="course", lazy="select")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    duration_minutes = Column(Integer)
    order = Column("order", Integer)
    lessons_structure_json = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", lazy="select")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    objectives_json = Column(String)
    mandatory_topics_json = Column(String)
    duration_minutes = Column(Integer)
    order = Column("order", Integer)
    sections_structure_json = Column(String)
    avatar_video_url = Column(String)
    mp4_video_url = Column(String)
    slides_pdf_url = Column(String)
    slides_and_avatar_video_url = Column(String)
    slides_and_audio_video_url = Column(String)
    lesson_type = Column(String, default="CONTENT")
    module_id = Column(Integer, ForeignKey("modules.id"))

    module = relationship("Module", back_populates="lessons")
    sections = relationship("Section", back_populates="lesson", lazy="select")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    title = Column(String)
    content = Column(String)
    prompt = Column(String)
    duration_minutes = Column(Integer)
    order = Column("order", Integer)
    audio_url = Column(String)
    audio_duration = Column(Float)
    raw_video_url = Column(String)
    avatar_video_url = Column(String)
    cloned_audio_url = Column(String)
    slides_and_avatar_video_url = Column(String)
    slide_audio_video_url = Column(String)
    section_pdf_url = Column(String)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))

    lesson = relationship("Lesson", back_populates="sections")
    slide = relationship("Slide", back_populates="section", uselist=False, lazy="select")


class Slide(Base):
    __tablename__ = "slides"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    contents_json = Column(String, nullable=False)

    section = relationship("Section", back_populates="slide")

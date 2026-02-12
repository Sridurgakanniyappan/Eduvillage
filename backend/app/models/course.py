from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    level = Column(String, nullable=True)
    is_approved = Column(Boolean, default=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))

    teacher = relationship("User", backref="courses_taught")
    subjects = relationship("Subject", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="subjects")

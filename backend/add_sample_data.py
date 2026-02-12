"""
Script to add sample course data with lessons and video URLs.
Run this from the backend directory: python add_sample_data.py
"""
from app.db.session import SessionLocal
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Check if we have a teacher user
        teacher = db.query(User).filter(User.role == "teacher").first()
        if not teacher:
            print("No teacher user found. Please create a teacher user first.")
            return
        
        # Create a sample course
        course = Course(
            title="Introduction to Web Development",
            description="Learn HTML, CSS, and JavaScript basics",
            category="Development",
            level="Beginner",
            teacher_id=teacher.id,
            is_approved=True
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        
        # Add lessons with video URLs
        lessons_data = [
            {
                "title": "HTML Basics",
                "content": "Learn the fundamentals of HTML including tags, elements, and structure.",
                "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE",
                "order": 1
            },
            {
                "title": "CSS Styling",
                "content": "Master CSS selectors, properties, and layout techniques.",
                "video_url": "https://www.youtube.com/watch?v=yfoY53QXEnI",
                "order": 2
            },
            {
                "title": "JavaScript Introduction",
                "content": "Get started with JavaScript variables, functions, and DOM manipulation.",
                "video_url": "https://www.youtube.com/watch?v=W6NZfCO5SIk",
                "order": 3
            }
        ]
        
        for lesson_data in lessons_data:
            lesson = Lesson(
                **lesson_data,
                course_id=course.id
            )
            db.add(lesson)
        
        db.commit()
        print(f"✅ Successfully created course '{course.title}' with {len(lessons_data)} lessons!")
        print(f"   Course ID: {course.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()

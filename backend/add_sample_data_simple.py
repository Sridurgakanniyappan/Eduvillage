"""
Simple script to add sample course data using raw SQL.
Run this: python add_sample_data_simple.py
"""
from app.db.session import engine
from sqlalchemy import text

def add_sample_data():
    try:
        with engine.connect() as conn:
            # First, check if we have a teacher
            result = conn.execute(text("SELECT id FROM users WHERE role = 'teacher' LIMIT 1"))
            teacher_row = result.fetchone()
            
            if not teacher_row:
                print("❌ No teacher user found. Please create a teacher user first.")
                print("   You can create one through the /api/auth/register endpoint")
                return
            
            teacher_id = teacher_row[0]
            
            # Insert a sample course
            result = conn.execute(text("""
                INSERT INTO courses (title, description, category, level, is_approved, teacher_id)
                VALUES (:title, :desc, :cat, :level, :approved, :teacher_id)
                RETURNING id
            """), {
                "title": "Introduction to Web Development",
                "desc": "Learn HTML, CSS, and JavaScript basics",
                "cat": "Development",
                "level": "Beginner",
                "approved": True,
                "teacher_id": teacher_id
            })
            course_id = result.fetchone()[0]
            
            # Insert lessons
            lessons = [
                ("HTML Basics", "Learn the fundamentals of HTML including tags, elements, and structure.", "https://www.youtube.com/watch?v=UB1O30fR-EE", 1),
                ("CSS Styling", "Master CSS selectors, properties, and layout techniques.", "https://www.youtube.com/watch?v=yfoY53QXEnI", 2),
                ("JavaScript Introduction", "Get started with JavaScript variables, functions, and DOM manipulation.", "https://www.youtube.com/watch?v=W6NZfCO5SIk", 3)
            ]
            
            for title, content, video_url, order in lessons:
                conn.execute(text("""
                    INSERT INTO lessons (title, content, video_url, "order", course_id)
                    VALUES (:title, :content, :video_url, :order, :course_id)
                """), {
                    "title": title,
                    "content": content,
                    "video_url": video_url,
                    "order": order,
                    "course_id": course_id
                })
            
            conn.commit()
            print(f"✅ Successfully created course 'Introduction to Web Development' with 3 lessons!")
            print(f"   Course ID: {course_id}")
            print(f"   Teacher ID: {teacher_id}")
            print("\nNow you can:")
            print("1. Enroll a student in this course")
            print("2. View the course with video lessons in the student dashboard")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_sample_data()

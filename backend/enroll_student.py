"""
Script to enroll a student in a course.
Run this: python enroll_student.py
"""
from app.db.session import engine
from sqlalchemy import text

def enroll_student():
    try:
        with engine.connect() as conn:
            # Get the first student
            result = conn.execute(text("SELECT id, email FROM users WHERE role = 'student' LIMIT 1"))
            student_row = result.fetchone()
            
            if not student_row:
                print("❌ No student user found. Please create a student user first.")
                return
            
            student_id = student_row[0]
            student_email = student_row[1]
            
            # Get the first course
            result = conn.execute(text("SELECT id, title FROM courses LIMIT 1"))
            course_row = result.fetchone()
            
            if not course_row:
                print("❌ No courses found. Please create a course first.")
                return
            
            course_id = course_row[0]
            course_title = course_row[1]
            
            # Check if already enrolled
            result = conn.execute(text("""
                SELECT id FROM enrollments 
                WHERE student_id = :student_id AND course_id = :course_id
            """), {"student_id": student_id, "course_id": course_id})
            
            if result.fetchone():
                print(f"ℹ️  Student {student_email} is already enrolled in '{course_title}'")
                return
            
            # Enroll the student
            conn.execute(text("""
                INSERT INTO enrollments (student_id, course_id)
                VALUES (:student_id, :course_id)
            """), {
                "student_id": student_id,
                "course_id": course_id
            })
            
            conn.commit()
            print(f"✅ Successfully enrolled student '{student_email}' in course '{course_title}'!")
            print(f"\nNow login as this student and go to 'My Courses' to see the course with videos!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    enroll_student()

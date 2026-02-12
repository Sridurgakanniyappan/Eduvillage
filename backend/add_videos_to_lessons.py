"""
Script to add video URLs to existing lessons in the database.
Run this: python add_videos_to_lessons.py
"""
from app.db.session import engine
from sqlalchemy import text

def add_videos_to_lessons():
    try:
        with engine.connect() as conn:
            # Get all lessons without video URLs
            result = conn.execute(text("""
                SELECT l.id, l.title, c.title as course_title 
                FROM lessons l
                JOIN courses c ON l.course_id = c.id
                WHERE l.video_url IS NULL OR l.video_url = ''
            """))
            
            lessons = result.fetchall()
            
            if not lessons:
                print("ℹ️  All lessons already have video URLs!")
                
                # Show existing lessons with videos
                result = conn.execute(text("""
                    SELECT l.id, l.title, l.video_url, c.title as course_title 
                    FROM lessons l
                    JOIN courses c ON l.course_id = c.id
                    WHERE l.video_url IS NOT NULL AND l.video_url != ''
                """))
                existing = result.fetchall()
                
                if existing:
                    print(f"\n📹 Found {len(existing)} lessons with videos:")
                    for lesson_id, title, video_url, course_title in existing:
                        print(f"   - {course_title} / {title}")
                        print(f"     Video: {video_url[:50]}...")
                return
            
            print(f"📝 Found {len(lessons)} lessons without videos:")
            for lesson_id, title, course_title in lessons:
                print(f"   - {course_title} / {title}")
            
            # Sample video URLs (you can customize these)
            sample_videos = [
                "https://www.youtube.com/watch?v=UB1O30fR-EE",  # HTML Tutorial
                "https://www.youtube.com/watch?v=yfoY53QXEnI",  # CSS Tutorial
                "https://www.youtube.com/watch?v=W6NZfCO5SIk",  # JavaScript Tutorial
                "https://www.youtube.com/watch?v=PkZNo7MFNFg",  # Learn Python
                "https://www.youtube.com/watch?v=rfscVS0vtbw",  # Learn Python Full Course
                "https://www.youtube.com/watch?v=8ext9G7xspg",  # React Tutorial
            ]
            
            # Add videos to lessons
            video_index = 0
            for lesson_id, title, course_title in lessons:
                video_url = sample_videos[video_index % len(sample_videos)]
                
                conn.execute(text("""
                    UPDATE lessons 
                    SET video_url = :video_url 
                    WHERE id = :lesson_id
                """), {
                    "video_url": video_url,
                    "lesson_id": lesson_id
                })
                
                print(f"\n✅ Added video to: {course_title} / {title}")
                print(f"   URL: {video_url}")
                
                video_index += 1
            
            conn.commit()
            print(f"\n🎉 Successfully added videos to {len(lessons)} lessons!")
            print("\nNow refresh your browser and check 'My Courses' to see the videos!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_videos_to_lessons()

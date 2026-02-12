"""
Migration script to add missing columns to courses table.
Run this once: python migrate_courses.py
"""
from app.db.session import SessionLocal, engine
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    
    try:
        # Add missing columns to courses table
        with engine.connect() as conn:
            # Check if columns exist and add them if they don't
            try:
                conn.execute(text("ALTER TABLE courses ADD COLUMN category VARCHAR"))
                print("✅ Added 'category' column")
            except Exception as e:
                print(f"   'category' column might already exist: {e}")
            
            try:
                conn.execute(text("ALTER TABLE courses ADD COLUMN level VARCHAR"))
                print("✅ Added 'level' column")
            except Exception as e:
                print(f"   'level' column might already exist: {e}")
            
            try:
                conn.execute(text("ALTER TABLE courses ADD COLUMN is_approved BOOLEAN DEFAULT FALSE"))
                print("✅ Added 'is_approved' column")
            except Exception as e:
                print(f"   'is_approved' column might already exist: {e}")
            
            conn.commit()
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .models import Base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Drop and recreate tables (for development)
def recreate_tables():
    """Drop all tables and recreate them - use only in development"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables recreated successfully.")

# Check if database needs migration
def check_database_schema():
    """Check if database schema matches current models"""
    import os
    
    # Check if database file exists
    db_file = "./chatbot.db"
    if not os.path.exists(db_file):
        print("📁 Database file not found. Creating new database...")
        create_tables()
        return True
    
    try:
        # Try to query the user_type column using proper SQLAlchemy syntax
        from sqlalchemy import text
        db = SessionLocal()
        result = db.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result.fetchall()]
        db.close()
        
        # Check if user_type column exists
        if 'user_type' not in columns:
            print("⚠️  Database schema outdated. Recreating tables...")
            recreate_tables()
            return True
        else:
            print("✅ Database schema is up to date.")
            return False
    except Exception as e:
        print(f"⚠️  Database check failed: {e}")
        print("Recreating database tables...")
        recreate_tables()
        return True

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
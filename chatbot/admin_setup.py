import os
import secrets
import string
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .auth import get_password_hash

def generate_secure_password(length: int = 16) -> str:
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_default_admin():
    """Create default admin account if it doesn't exist"""
    # Get admin details from environment variables
    admin_first_name = os.getenv("ADMIN_FIRST_NAME", "Admin")
    admin_last_name = os.getenv("ADMIN_LAST_NAME", "Officer")
    admin_username = os.getenv("ADMIN_USERNAME", "admin_user")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@oui.edu.ng")
    
    # Get password from environment
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password:
        admin_password = generate_secure_password()
        print(f"⚠️  No ADMIN_PASSWORD found in .env file")
        print(f"Generated admin password: {admin_password}")
        print("Please set ADMIN_PASSWORD in your .env file for production use.")
    else:
        print(f"✅ Using admin password from .env file")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(
            (User.username == admin_username) | (User.email == admin_email)
        ).first()
        
        if existing_admin:
            print(f"Admin user '{admin_username}' already exists.")
            return existing_admin
        
        # Create new admin user
        hashed_password = get_password_hash(admin_password)
        admin_user = User(
            username=admin_username,
            email=admin_email,
            first_name=admin_first_name,
            last_name=admin_last_name,
            user_type="admin",
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Admin user created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Name: {admin_first_name} {admin_last_name}")
        print(f"   Password: {admin_password}")
        print(f"   User Type: {admin_user.user_type}")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return None
    finally:
        db.close() 
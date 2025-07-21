#!/usr/bin/env python3
"""
Database reset script for development
"""

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.database import recreate_tables
from chatbot.admin_setup import create_default_admin

def main():
    """Reset database and create admin user"""
    print("🔄 Resetting database...")
    
    try:
        # Recreate all tables
        recreate_tables()
        
        # Create default admin
        print("👤 Creating default admin user...")
        admin_user = create_default_admin()
        
        if admin_user:
            print("✅ Database reset completed successfully!")
            print("✅ Admin user created successfully!")
        else:
            print("❌ Failed to create admin user")
            
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
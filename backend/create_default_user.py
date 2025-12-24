"""
Script to create a default admin user
Run this script to create a default admin account for testing
"""

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_default_user():
    """Create default admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@botboss.com").first()
        if admin:
            print("❌ Admin user already exists!")
            print(f"   Email: admin@botboss.com")
            print("   Use the existing account or register a new one.")
            return
        
        # Create default admin
        admin_user = User(
            email="admin@botboss.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Default admin user created successfully!")
        print("\n📧 Login Credentials:")
        print("   Email: admin@botboss.com")
        print("   Password: admin123")
        print("\n⚠️  IMPORTANT: Change this password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating default admin user...")
    create_default_user()


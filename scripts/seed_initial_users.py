import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

def seed_users():
    db = SessionLocal()
    try:
        sample_users = [
            {
                "email": "admin@gimpa.edu.gh",
                "password": "Password123!",
                "full_name": "System Administrator",
                "role": "admin",
                "roles": ["system_admin", "librarian"],
                "is_admin": True,
                "school": "School of Technology and Social Sciences",
                "department": "Computer Science"
            },
            {
                "email": "dean@gimpa.edu.gh",
                "password": "Password123!",
                "full_name": "Dr. Dean",
                "role": "dean",
                "roles": ["dean", "lecturer"],
                "is_admin": False,
                "school": "School of Technology and Social Sciences",
                "department": "Computer Science"
            },
            {
                "email": "hod@gimpa.edu.gh",
                "password": "Password123!",
                "full_name": "Dr. HOD",
                "role": "hod",
                "roles": ["hod", "lecturer"],
                "is_admin": False,
                "school": "School of Technology and Social Sciences",
                "department": "Computer Science"
            },
            {
                "email": "lecturer@gimpa.edu.gh",
                "password": "Password123!",
                "full_name": "Prof. Lecturer",
                "role": "lecturer",
                "roles": ["lecturer"],
                "is_admin": False,
                "school": "School of Technology and Social Sciences",
                "department": "Computer Science"
            },
            {
                "email": "student@st.gimpa.edu.gh",
                "password": "Password123!",
                "full_name": "Student Scholar",
                "role": "student",
                "roles": ["student"],
                "is_admin": False,
                "student_id": "ST-2026-001",
                "school": "School of Technology and Social Sciences",
                "department": "Computer Science"
            }
        ]

        for u_data in sample_users:
            existing = db.query(User).filter(User.email == u_data["email"]).first()
            if not existing:
                u = User(
                    email=u_data["email"],
                    password_hash=hash_password(u_data["password"]),
                    full_name=u_data["full_name"],
                    role=u_data["role"],
                    roles=json.dumps(u_data["roles"]),
                    is_admin=u_data["is_admin"],
                    school=u_data.get("school"),
                    department=u_data.get("department"),
                    student_id=u_data.get("student_id"),
                    is_active=True,
                    is_verified=True
                )
                db.add(u)
                print(f"[+] Seeded user: {u_data['email']} (Role: {u_data['role']})")
            else:
                print(f"[*] User {u_data['email']} already exists.")

        db.commit()
        print("[SUCCESS] Seeding completed successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()\n
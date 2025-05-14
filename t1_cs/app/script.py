from datetime import date
from app.database import SessionLocal
from app.models.profile import Profile
from app.models.user import User
from sqlalchemy.orm import Session

def populate_profiles_and_user(db: Session):
    profiles_exist = db.query(Profile).count() > 0
    
    if not profiles_exist:
        profiles = [
            Profile(name="Admin"),
            Profile(name="Professor"),
            Profile(name="Coordinator"),
        ]
        db.add_all(profiles)
        db.commit()
        print("Profiles criados.")

    admin_profile = db.query(Profile).filter_by(name="Admin").first()
    if not admin_profile:
        print("Profile Admin não encontrado.")
        return

    sofia_exists = db.query(User).filter_by(name="Sofia").first()
    if not sofia_exists:
        sofia = User(
            email="sofia@example.com",
            name="Sofia",
            birth_date=date(1990, 1, 1), 
            gender="Feminino",
            profile_id=admin_profile.id
        )
        db.add(sofia)
        db.commit()
        print("Usuário Sofia criado.")
    else:
        print("Usuário Sofia já existe.")



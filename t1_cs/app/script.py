from datetime import date
from sqlalchemy.orm import Session
from app.database import SessionLocal

from app.models.profile import Profile
from app.models.user import User
from app.models.building import Building
from app.models.room import Room
from app.models.class_model import Class
from app.models.curriculum import Curriculum
from app.models.evaluation import Evaluation
from app.models.resource_type import ResourceType
from app.models.discipline import Discipline
from app.models.lesson import Lesson
from app.models.resource import Resource
from app.models.reservation import Reservation


def populate_profiles_and_user(db: Session):
    if db.query(Profile).count() == 0:
        profiles = [
            Profile(name="Admin"),
            Profile(name="Professor"),
            Profile(name="Coordinator"),
        ]
        db.add_all(profiles)
        db.commit()
        print("Perfis criados com sucesso.")
    else:
        print("Perfis já existem.")

    admin_profile = db.query(Profile).filter_by(name="Admin").first()
    if not admin_profile:
        print("Erro: perfil Admin não encontrado.")
        return

    if not db.query(User).filter_by(name="Sofia").first():
        sofia = User(
            email="sofia@example.com",
            name="Sofia",
            birth_date=date(1990, 1, 1), 
            gender="Feminino",
            profile_id=admin_profile.id
        )
        db.add(sofia)
        db.commit()
        print("Usuária Sofia criada com sucesso.")
    else:
        print("Usuária Sofia já existe.")
        
    if db.query(Building).count() <= 3:
    
        buildings = [
            Building(name="Building A", building_number=1, street="Main St", number="100", complement="Block A", neighborhood="Downtown", city="CityX", state="XX", postal_code="12345-000"),
            Building(name="Building B", building_number=2, street="Second St", number="200", complement="", neighborhood="Uptown", city="CityY", state="YY", postal_code="23456-111"),
            Building(name="Building C", building_number=3, street="Third St", number="300", complement="Annex", neighborhood="Midtown", city="CityZ", state="ZZ", postal_code="34567-222"),
        ]

        for building in buildings:
            existing_building = db.query(Building).filter_by(building_number=building.building_number).first()
            if not existing_building:
                db.add(building)
                print(f"Prédio {building.name} criado.")
            else:
                print(f"Prédio {building.name} já existe.")

        db.commit()
        print("Prédios criados.")


def populate_all(db: Session):
    if db.query(Room).count() <= 0:
        buildings = db.query(Building).all()
        if len(buildings) < 3:
            print("Erro: número insuficiente de prédios para criar salas.")
            return
        rooms = [
            Room(room_number=101, capacity=30, floor="1", building_id=buildings[0].id),
            Room(room_number=201, capacity=40, floor="2", building_id=buildings[1].id),
            Room(room_number=301, capacity=50, floor="3", building_id=buildings[2].id),
        ]
        for room in rooms:
            existing_room = db.query(Room).filter_by(room_number=room.room_number, building_id=room.building_id).first()
            if not existing_room:
                db.add(room)
                print(f"Sala {room.room_number} criada.")
            else:
                print(f"Sala {room.room_number} já existe.")
        db.commit()

    if db.query(ResourceType).count() <= 3:
        types = [
            ResourceType(name="Projector"),
            ResourceType(name="Whiteboard"),
            ResourceType(name="Computer"),
        ]
        for resource_type in types:
            existing_type = db.query(ResourceType).filter_by(name=resource_type.name).first()
            if not existing_type:
                db.add(resource_type)
                print(f"Tipo de recurso {resource_type.name} criado.")
            else:
                print(f"Tipo de recurso {resource_type.name} já existe.")
        db.commit()

    if db.query(Resource).count() <= 3:
        types = db.query(ResourceType).all()
        if len(types) < 3:
            print("Erro: número insuficiente de tipos de recursos.")
            return
        resources = [
            Resource(description="Projector Epson", status="available", resource_type_id=types[0].id),
            Resource(description="Whiteboard Large", status="available", resource_type_id=types[1].id),
            Resource(description="MacBook Pro", status="maintenance", resource_type_id=types[2].id),
        ]
        for resource in resources:
            existing_resource = db.query(Resource).filter_by(description=resource.description).first()
            if not existing_resource:
                db.add(resource)
                print(f"Recurso {resource.description} criado.")
            else:
                print(f"Recurso {resource.description} já existe.")
        db.commit()

    if db.query(Discipline).count() <= 3:
        disciplines = [
            Discipline(name="Math 101", credits=4, program="Algebra and Calculus", bibliography="Math Book A"),
            Discipline(name="Physics 201", credits=3, program="Mechanics", bibliography="Physics Book B"),
            Discipline(name="CS 301", credits=5, program="Data Structures", bibliography="CS Book C"),
        ]
        for discipline in disciplines:
            existing_discipline = db.query(Discipline).filter_by(name=discipline.name).first()
            if not existing_discipline:
                db.add(discipline)
                print(f"Disciplina {discipline.name} criada.")
            else:
                print(f"Disciplina {discipline.name} já existe.")
        db.commit()

    if db.query(Curriculum).count() <= 3:
        curriculums = [
            Curriculum(course_name="Engineering", start_date=date(2020, 1, 1)),
            Curriculum(course_name="Physics", start_date=date(2021, 1, 1)),
            Curriculum(course_name="Computer Science", start_date=date(2022, 1, 1)),
        ]
        for curriculum in curriculums:
            existing_curriculum = db.query(Curriculum).filter_by(course_name=curriculum.course_name).first()
            if not existing_curriculum:
                db.add(curriculum)
                print(f"Currículo {curriculum.course_name} criado.")
            else:
                print(f"Currículo {curriculum.course_name} já existe.")
        db.commit()

        all_disciplines = db.query(Discipline).all()
        for curriculum in curriculums:
            curriculum.disciplines = all_disciplines
        db.commit()
        print("Currículos e disciplinas associados.")

    if db.query(Class).count() <= 3:
        disciplines = db.query(Discipline).all()
        professor = db.query(User).filter_by(name="Sofia").first()
        if not professor:
            print("Erro: professora Sofia não encontrada.")
            return
        classes = [
            Class(semester="2024/1", schedule="Mon-Wed 10:00-12:00", vacancies=40, discipline_id=disciplines[0].id, professor_id=professor.id),
            Class(semester="2024/1", schedule="Tue-Thu 14:00-16:00", vacancies=35, discipline_id=disciplines[1].id, professor_id=professor.id),
            Class(semester="2024/1", schedule="Fri 08:00-12:00", vacancies=25, discipline_id=disciplines[2].id, professor_id=professor.id),
        ]
        for class_instance in classes:
            existing_class = db.query(Class).filter_by(semester=class_instance.semester, schedule=class_instance.schedule).first()
            if not existing_class:
                db.add(class_instance)
                print(f"Turma {class_instance.semester} criada.")
            else:
                print(f"Turma {class_instance.semester} já existe.")
        db.commit()

    print("Banco de dados populado com sucesso.")

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20))
    address = Column(String(200))
    skills = Column(String(200))
    experience = Column(String(200))
    specialization = Column(String(100))
    about = Column(String(1000))

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(100), nullable=False)
    specialization = Column(String(100))
    number_of_people_required = Column(Integer)
    expiry = Column(Date)
    county = Column(String(100))
    city = Column(String(100))
    salary = Column(Integer)
    minimum_qualifications = Column(String(200))
    experience_required = Column(String(200))
    contact_email = Column(String(120))
    contact_phone = Column(String(20))
    contact_person = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="jobs")

class Agency(Base):
    __tablename__ = "agencies"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    license_validity = Column(Date, nullable=False)
    county = Column(String(100))
    constituency = Column(String(100))
    town = Column(String(100))
    director_name = Column(String(100))
    director_contact = Column(String(20))
    manager_name = Column(String(100))
    manager_contact = Column(String(20))
    hr_name = Column(String(100))
    hr_contact = Column(String(20))

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    company_type = Column(String(100))
    registration_number = Column(String(100))
    county = Column(String(100))
    city = Column(String(100))
    email = Column(String(120))
    physical_address = Column(String(200))
    director_name = Column(String(100))
    director_contact = Column(String(20))
    key_contact_person_name = Column(String(100))
    key_contact_person_contact = Column(String(20))
    hr_name = Column(String(100))
    hr_contact = Column(String(20))


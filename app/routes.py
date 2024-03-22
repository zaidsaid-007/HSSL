from flask import Flask, jsonify, request
from .models import User, Job, Company, Agency, Base
from sqlalchemy.orm import sessionmaker
from .database import engine
from werkzeug.security import generate_password_hash, check_password_hash

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
Session = sessionmaker(bind=engine)

# User Registration Endpoint
@app.route("/users", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username and email and password):
        return jsonify({"error": "Username, email, and password are required"}), 400

    hashed_password = generate_password_hash(password)

    session = Session()
    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.close()

    return jsonify({"message": "User registered successfully"}), 201

# User Login Endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username_or_email = data.get("username_or_email")
    password = data.get("password")

    if not (username_or_email and password):
        return jsonify({"error": "Username/email and password are required"}), 400

    session = Session()
    user = session.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if not (user and check_password_hash(user.password, password)):
        return jsonify({"error": "Invalid username/email or password"}), 401

    
    return jsonify({"message": "Login successful"}), 200

# Company Management Routes
@app.route("/companies", methods=["POST"])
def register_company():
    data = request.json
    company = Company(**data)
    session = Session()
    session.add(company)
    session.commit()
    session.close()

    return jsonify({"message": "Company registered successfully"}), 201

@app.route("/companies", methods=["GET"])
def get_companies():
    session = Session()
    companies = session.query(Company).all()
    session.close()

    company_list = [{"id": company.id, "name": company.name, "email": company.email} for company in companies]
    return jsonify(company_list), 200

# Agency Management Routes
@app.route("/agencies", methods=["POST"])
def register_agency():
    data = request.json
    agency = Agency(**data)
    session = Session()
    session.add(agency)
    session.commit()
    session.close()

    return jsonify({"message": "Agency registered successfully"}), 201

@app.route("/agencies", methods=["GET"])
def get_agencies():
    session = Session()
    agencies = session.query(Agency).all()
    session.close()

    agency_list = [{"id": agency.id, "name": agency.name, "email": agency.email} for agency in agencies]
    return jsonify(agency_list), 200

# Post Job Endpoint
@app.route("/jobs", methods=["POST"])
def post_job():
    data = request.json

    # Authentication check (implement as needed)

    # Validate job data
    required_fields = ["title", "description", "budget"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Title, description, and budget are required"}), 400

    session = Session()
    job = Job(**data)
    session.add(job)
    session.commit()
    session.close()

    return jsonify({"message": "Job posted successfully"}), 201

# Get All Jobs Endpoint
@app.route("/jobs", methods=["GET"])
def get_all_jobs():
    session = Session()
    jobs = session.query(Job).all()
    session.close()

    job_list = [{"id": job.id, "title": job.title, "description": job.description, "budget": job.budget} for job in jobs]
    return jsonify(job_list), 200

# Get Specific Job Endpoint
@app.route("/jobs/<int:job_id>", methods=["GET"])
def get_specific_job(job_id):
    session = Session()
    job = session.query(Job).filter_by(id=job_id).first()
    session.close()

    if not job:
        return jsonify({"error": "Job not found"}), 404

    job_details = {"id": job.id, "title": job.title, "description": job.description, "budget": job.budget}
    return jsonify(job_details), 200


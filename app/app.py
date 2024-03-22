from flask import Flask, jsonify, request
from .models import User, Job, Base
from sqlalchemy.orm import sessionmaker
from .database import engine

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

Session = sessionmaker(bind=engine)


# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# User Endpoints

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    phone_number = data.get("phone_number")
    address = data.get("address")

    if not (username and email):
        return jsonify({"error": "Username and email are required"}), 400

    session = Session()
    user = User(username=username, email=email, phone_number=phone_number, address=address)
    session.add(user)
    session.commit()
    session.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.address = data.get("address", user.address)

    session.commit()
    session.close()

    return jsonify({"message": "User details updated successfully"})


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    session.delete(user)
    session.commit()
    session.close()

    return jsonify({"message": "User deleted successfully"})


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_details = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address
    }

    session.close()

    return jsonify(user_details)


# Job Endpoints

@app.route("/job", methods=["POST"])
def post_job():
    data = request.json
    required_fields = ["order_number", "date", "category"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Order number, date, and category are required"}), 400

    session = Session()
    job = Job(**data)
    session.add(job)
    session.commit()
    session.close()

    return jsonify({"message": "Job posted successfully"}), 201


@app.route("/jobs", methods=["GET"])
def list_jobs():
    session = Session()
    jobs = session.query(Job).all()

    job_list = []
    for job in jobs:
        job_details = {
            "id": job.id,
            "order_number": job.order_number,
            "date": job.date,
            "category": job.category,
            "specialization": job.specialization,
            "number_of_people_required": job.number_of_people_required,
            "expiry": job.expiry,
            "county": job.county,
            "city": job.city,
            "salary": job.salary,
            "minimum_qualifications": job.minimum_qualifications,
            "experience": job.experience,
            "contact_email": job.contact_email,
            "contact_phone": job.contact_phone,
            "contact_person": job.contact_person,
            "user_id": job.user_id
        }
        job_list.append(job_details)

    session.close()

    return jsonify(job_list)


if __name__ == "__main__":
    app.run(debug=True)

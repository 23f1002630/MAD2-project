from flask import Flask, url_for
from flask import jsonify
from flask import request
from database import db
from models import *
from models import user as User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, set_access_cookies
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from celery.schedules import crontab
# from config import LocalDevelopmentConfig
from celery import Celery
from send_mail import init_mail
from flask_mail import Message
from flask_sse import sse
from functools import wraps
import os

from cache import Cache


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = 'secret@1234'
# Setup the Flask-JWT-Extended extension
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housedatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "5#y2LF4Q8z\n\xec]/"  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # CHANGE NEW
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'

cache = Cache(app)

# CORS(app, supports_credentials=True)
CORS(app, origins='http://localhost:5173', supports_credentials=True)
jwt = JWTManager(app)
db.init_app(app)
app.app_context().push()
db.create_all()


admin_exist = User.query.filter_by(email="hisham@gmail.com").first()
if not admin_exist:
    user = User(email="hisham@gmail.com",
                password=generate_password_hash("hisham999"))
    db.session.add(user)
    db.session.commit()

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
# @app.route("/api/login", methods=["POST"])
# def login():
#     print('Entered login API')
#     # Get JSON data from the request
#     data = request.get_json()
#     email = data.get("email", None)
#     password = data.get("password", None)
#     role=data.get("role",None)

#     if not email or not password:
#         return jsonify(error="Email and password are required"), 400

#     # Log the received email and password
#     print(f"Login attempt: email={email}, password={password}")
#     if role=="admin":
#     admin_exist = User.query.filter_by(email="hisham@gmail.com").first()
#     if not admin_exist:
#         user= User(email="hisham@gmail.com",
#                 password=generate_password_hash("hisham999"))
#         db.session.add(user)
#         db.session.commit()
#     user=User.query.filter_by(email=email).first()
#     if user:
#         # Verify the password
#         if check_password_hash(user.password, password):
#             # Create an access token for the user
#             access_token = create_access_token(identity=user.email)
#             response = jsonify(access_token=access_token)
#             # Set access token cookies in the response
#             set_access_cookies(response, access_token)
#             return response
#         else:
#             # Return error if the password is incorrect
#             return jsonify(error="Invalid credentials"), 401
#     else:
#         # Return error if the user doesn't exist
#         return jsonify(error="User not found"), 404

# ------- Celery app ------- #
celery = Celery('Application')

# Update celery app configurations
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
)
celery.conf.timezone = 'Asia/Kolkata'


@celery.task()
def monthly_report():
    print('monthly report to users executed')
    return {'message': "Monthly report to users executed"}


@celery.task()
def user_triggered_async_job():
    print('user triggered async job executed')
    return {'message': "User triggered async job executed"}


# ------- To schedule the tasks --------#
celery.conf.beat_schedule = {
    'my_daily_task': {
        'task': "main.monthly_report",
        'schedule': crontab(hour=21, minute=0),
    },
    'my_quick_check_task': {
        'task': "main.monthly_report",
        'schedule': crontab(minute='*/1'),
    },
}


@app.route("/api/login", methods=["POST"])
def login():
    print('Entered login API')
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    role = data.get("role", None)

    if not email or not password:
        return jsonify(error="Email and password are required"), 400

    print(f"Login attempt: email={email}, password={password}, role={role}")

    if role == "admin":
        user = User.query.filter_by(email=email).first()
    elif role == "customer":
        user = Customer.query.filter_by(emailid=email, isblocked=0).first()
    elif role == "provider":
        user = Provider.query.filter_by(
            emailid=email, isblocked=0, status="Approved").first()
    else:
        return jsonify(error="Invalid role"), 400

    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            response = jsonify(access_token=access_token)
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify(error="Invalid credentials"), 401
    else:
        return jsonify(error="User not found"), 404

    # create a function called services --services table query all-- list=[ define all the required colmns in json format] --return jsonify(list)--try catch return json status codes
    # this.listname=response.data  /// data return listname=[] ///for key,index in listname


@app.route("/customer/register", methods=['POST'])
def cust_reg():
    if request.method != "POST":
        return jsonify({"error": "Invalid request method"}), 405
    data = request.get_json()
    emailid = data.get("emailid")
    password = data.get("password")
    fullname = data.get("fullname")
    phone = data.get("phone")
    address = data.get("address")
    pincode = data.get("pincode")

    # Validate required fields
    if not password or password.strip() == "":
        return jsonify({"error": "Password cannot be empty"}), 400
    if not fullname or fullname.strip() == "":
        return jsonify({"error": "Full name cannot be empty"}), 400
    if not phone:
        return jsonify({"error": "Phone number cannot be empty"}), 400

    # Check if email or phone already exists
    if Customer.query.filter_by(emailid=emailid).first():
        return jsonify({"error": "Customer email already exists"}), 400
    if Customer.query.filter_by(phone=phone).first():
        return jsonify({"error": "Phone number already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new customer
    new_customer = Customer(
        emailid=emailid,
        password=hashed_password,
        fullname=fullname,
        phone=phone,
        address=address,
        pincode=pincode
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"msg": "Registration successful", "emailid": emailid}), 201

# @app.route('/customer/register', methods=['POST'])
# def customer():
#     if request.method == "" :
#         user = Customer.query.filter_by(id==user_id).first()
#         if user == None:
#             return "Not found", 404
#         else :
#             return {"email":user.email,"phone" :user.phone} , 201

#     elif request.method == "POST" :
#             data = request.get_json()
#             email = data.email
#             password = data.password
#             phone = data.phone
#             address = data.address
#             pincode = data.pincode

#             user  = customer(email=email, password=generate_password_hash(password), phone = phone, address = address, pincode = pincode )
#             db.session.add(user)
#             db.session.commit()

#     elif request.method == "PUT" :
#         data = request.get_json
#         email = data.email
#         password = data.password
#         phone = data.phone
#         address = data.address
#         pincode = data.pincode

# old one
# @app.route("/provider/register", methods=['POST'])
# def provider_reg():
#     if request.method != "POST":
#         return jsonify({"error": "Invalid request method"}), 405

#     data = request.get_json()
#     emailid = data.get("emailid")
#     password = data.get("password")
#     fullname = data.get("fullname")
#     phone = data.get("phone")
#     address = data.get("address")
#     pincode = data.get("pincode")
#     services = data.get("services")
#     experience = data.get("experience")
#     file = data.get("file")

#     # Validate required fields
#     if not password or password.strip() == "":
#         return jsonify({"error": "Password cannot be empty"}), 400
#     if not fullname or fullname.strip() == "":
#         return jsonify({"error": "Full name cannot be empty"}), 400
#     if not phone:
#         return jsonify({"error": "Phone number cannot be empty"}), 400
#     if not services:
#         return jsonify({"error": "Services cannot be empty"}), 400
#     if not experience:
#         return jsonify({"error": "Experience cannot be empty"}), 400

#     # Check if email or phone already exists
#     print('emailid', emailid)
#     if Provider.query.filter_by(emailid=emailid).first():
#         return jsonify({"error": "Provider email already exists"}), 400
#     if Provider.query.filter_by(phone=phone).first():
#         return jsonify({"error": "Phone number already exists"}), 400

#     # Hash the password
#     hashed_password = generate_password_hash(password)

#     # Create a new provider
#     new_provider = Provider(
#         emailid=emailid,
#         password=hashed_password,
#         fullname=fullname,
#         phone=phone,
#         address=address,
#         pincode=pincode,
#         services=services,
#         experience=experience,
#         file = file
#     )

#     db.session.add(new_provider)
#     db.session.commit()

#     return jsonify({"msg": "Provider registration successful", "emailid": emailid}), 201


@app.route("/provider/register", methods=['POST'])
def provider_reg():
    if request.method != "POST":
        return jsonify({"error": "Invalid request method"}), 405

    # Get form data
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    fullname = request.form.get("fullname")
    phone = request.form.get("phone")
    address = request.form.get("address")
    pincode = request.form.get("pincode")
    services = request.form.get("services")
    experience = request.form.get("experience")
    file = request.files.get("file")
    image = request.files.get("image")
    print('image', image, emailid)

    # Validate required fields
    if not password or password.strip() == "":
        return jsonify({"error": "Password cannot be empty"}), 400
    if not fullname or fullname.strip() == "":
        return jsonify({"error": "Full name cannot be empty"}), 400
    if not phone:
        return jsonify({"error": "Phone number cannot be empty"}), 400
    if not services:
        return jsonify({"error": "Services cannot be empty"}), 400
    if not experience:
        return jsonify({"error": "Experience cannot be empty"}), 400

    # Check if email or phone already exists
    if Provider.query.filter_by(emailid=emailid).first():
        return jsonify({"error": "Provider email already exists"}), 400
    if Provider.query.filter_by(phone=phone).first():
        return jsonify({"error": "Phone number already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Save the file if it exists
    if file:
        filename = fullname.replace(' ', '_') + '.pdf'
        file_path = os.path.join('static', filename)
        file.save(file_path)
    else:
        return jsonify({"error": "File is required"}), 400

    if image:
        filename = fullname.replace(' ', '_') + '.jpg'
        image_path = os.path.join('static', filename)
        image.save(image_path)
        print('image_path', image_path)
    else:
        return jsonify({"error": "Image is required"}), 400
    # Create a new provider
    new_provider = Provider(
        emailid=emailid,
        password=hashed_password,
        fullname=fullname,
        phone=phone,
        address=address,
        pincode=pincode,
        services=services,
        experience=experience,
        file=file_path,
        image=image_path
    )

    db.session.add(new_provider)
    db.session.commit()

    return jsonify({"msg": "Provider registration successful", "emailid": emailid}), 201


def method_name():
    pass
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.


@app.route("/api/professionals", methods=["GET"])
@jwt_required()
def get_professionals():
    try:
        professionals = Provider.query.all()
        professionals_list = [
            {
                "id": professional.id,
                "name": professional.fullname,
                "experience": professional.experience,
                "service_name": professional.services,
                "status": professional.status,
                "file": professional.file,
                "image": professional.image
            }
            for professional in professionals
        ]
        return jsonify(professionals_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/services", methods=["GET"])
@jwt_required()
def get_services():
    try:
        services = Services.query.all()
        services_list = [
            {
                "id": service.id,
                "services": service.services,
                "description": service.description,
                "price": service.price
            }
            for service in services
        ]
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# function for getting details of single service for editing/view purpose
@app.route('/api/services/<id>', methods=["GET"])
@jwt_required()
def get_service_details(id):
    try:
        service = Services.query.get(id)
        service_details = {
            "id": service.id,
            "services": service.services,
            "description": service.description,
            "price": service.price
        }

        return jsonify(service_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/professionalblock/<id>', methods=["POST"])
@jwt_required()
def block_professional(id):
    try:
        professional = Provider.query.get(id)
        professional.isblock = not professional.isblock
        db.session.commit()
        return jsonify({"message": "Professional blocked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/customerblock/<id>', methods=["POST"])
@jwt_required()
def block_customer(id):
    try:
        customer = Customer.query.get(id)
        customer.isblock = not customer.isblock
        db.session.commit()
        return jsonify({"message": "Customer blocked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/deleteprofessional/<id>', methods=["DELETE"])
@jwt_required()
def delete_professional(id):
    try:
        professional = Provider.query.get(id)
        db.session.delete(professional)
        db.session.commit()
        return jsonify({"message": "Professional deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/deletecustomer/<id>', methods=["DELETE"])
@jwt_required()
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/approveprofessional/<id>', methods=["POST"])
@jwt_required(id)
def approve_professional(id):
    try:
        print('id', id)
        professional = Provider.query.get(id)
        professional.status = "Approved"
        print('professional', professional)
        db.session.commit()
        return jsonify({"message": "Professional approved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/rejectprofessional/<id>', methods=["POST"])
@jwt_required()
def reject_professional(id):
    try:
        professional = Provider.query.get(id)
        professional.status = "Rejected"
        db.session.commit()
        return jsonify({"message": "Professional rejected successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/services/<id>', methods=["PUT"])
@jwt_required()
def update_service(id):
    try:
        # fetched service with id
        service = Services.query.get(id)
        # get form data
        data = request.json
        # editing values of db data
        service.services = data.get('services')
        service.description = data.get('description')
        service.price = data.get('price')
        # saving new data to db
        db.session.commit()
        service_data = {
            "id": service.id,
            "services": service.services,
            "description": service.description,
            "price": service.price,
        }
        return jsonify(service_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    service = Services.query.get(service_id)
    if service is None:
        return jsonify({'error': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200


@app.route('/api/services', methods=['POST'])
def add_service():
    data = request.json
    service_name = data.get('service')
    description = data.get('description')
    price = data.get('price')

    if not service_name or not description or not price:
        return jsonify({'error': 'Missing data'}), 400

    new_service = Services(services=service_name,
                           description=description, price=price)
    db.session.add(new_service)
    db.session.commit()

    return jsonify({'id': new_service.id, 'service': new_service.services, 'description': new_service.description, 'price': new_service.price}), 201


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run()

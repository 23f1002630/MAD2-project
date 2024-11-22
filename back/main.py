from flask import Flask, url_for
from flask import jsonify
from flask import request
from database import db
from sqlalchemy import and_, desc
from models import *
from models import user as User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, set_access_cookies, current_user
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

from flask_caching import Cache


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
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/0"
app.config['REDIS_URL'] = "redis://localhost:6379/3"
cache = Cache(app)


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


@jwt.user_identity_loader
def user_identity_lookup(user):
    print('user_identity_lookup', user)
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    print('jwt_data', jwt_data)
    identity = jwt_data["sub"]
    if identity is None:
        return None
    elif identity['role'] == 'admin':
        return User.query.filter_by(id=identity['user_id']).first()
    elif identity['role'] == 'customer':
        return Customer.query.filter_by(id=identity['user_id']).first()
    elif identity['role'] == 'provider':
        return Provider.query.filter_by(id=identity['user_id']).first()
    else:
        return None


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print('decorator called')
            if (current_user.__tablename__ == 'user'):
                current_user_role = 'admin'
            elif (current_user.__tablename__ == 'customer'):
                current_user_role = 'customer'
            elif (current_user.__tablename__ == 'provider'):
                current_user_role = 'provider'
            print('current_user_role', current_user_role)
            print('role', role)
            if current_user is None or current_user_role not in role:
                return {"message": "Unauthorized"}, 401
            print('Hisham called')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


mail = init_mail()


@celery.task()
def daily_reminder_to_professional():
  with app.app_context():
      professionals = Provider.query.all()
      for prof in professionals:
          # Check if there are any pending bookings for the professional
          pending_booking_exists = Booking.query.filter_by(provider_id=prof.id, status='pending').first() is not None

          if pending_booking_exists:
              with mail.connect() as conn:
                  subject = "Home Master Reminder"
                  message = """
                      <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                          <h1 style="color: #28a745;">Reminder: Visit Home Master</h1>
                          <p>This is a friendly reminder to visit Home Master and check your pending requests. Customers are waiting for you!</p>
                          <p>Don't miss out any requests. Click the link below to start your Home Master
                              experience:</p>
                          <a href="http://127.0.0.1:5000/" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: #fff; text-decoration: none; border-radius: 5px;">Visit Home Master</a>
                          <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
                          <p>Thank you for choosing Home Master!</p>
                          <p>Best regards,<br>Home Master</p>
                      </div>
                      """
                  msg = Message(recipients=[prof.emailid], html=message, subject=subject)
                  conn.send(msg)

              sse.publish({"message": "You have not placed any order, please place now!", "color": "alert alert-primary"}, type=prof.emailid)

      print('Daily reminder to users executed')
      return {"status": "success"}

celery.conf.beat_schedule = {
    'daily': {
      'task': 'main.daily_reminder_to_professional',  # Ensure this is the correct path to your task
      'schedule': crontab(minute='*'),
  }
}

@celery.task()
def monthly_report():
    print('monthly report to users executed')
    return {'message': "Monthly report to users executed"}


@celery.task()
def user_triggered_async_job():
    print('user triggered async job executed')
    return {'message': "User triggered async job executed"}


# ------- To schedule the tasks --------#
# celery.conf.beat_schedule = {
#     'my_daily_task': {
#         'task': "main.monthly_report",
#         'schedule': crontab(hour=21, minute=0),
#     },
#     'my_quick_check_task': {
#         'task': "main.monthly_report",
#         'schedule': crontab(minute='*/1'),
#     },
# }


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
            access_token = create_access_token(
                identity={'user_id': user.id, 'role': role}),
            response = jsonify(access_token=access_token, id=user.id)
            # set_access_cookies(response, access_token)

            return response, 200
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
        service_id=services,
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
@role_required(["admin"])
def get_professionals():
    try:
        professionals = Provider.query.all()
        professionals_list = [
            {
                "id": professional.id,
                "name": professional.fullname,
                "experience": professional.experience,
                "service_name": Services.query.get(professional.service_id).services,
                "status": professional.status,
                "file": professional.file,
                "image": professional.image,
                "isblocked": professional.isblocked
            }
            for professional in professionals
        ]
        return jsonify(professionals_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/customers", methods=["GET"])
@jwt_required()
@role_required(["admin", "customer"])
def get_customers():
    try:
        customers = Customer.query.all()
        customers_list = [
            {
                "id": customer.id,
                "name": customer.fullname,
                "email": customer.emailid,
                "phone": customer.phone,
                "address": customer.address,
                "pincode": customer.pincode,
                "isblocked": customer.isblocked
            }
            for customer in customers
        ]
        return jsonify(customers_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route("/api/customer/profile", methods=["GET"])
# @jwt_required()
# def get_customer_profile():
#     try:
#         customer = Customer.query.get(current_user.id)
#         customer_profile = {
#             "id": customer.id,
#             "name": customer.fullname,
#             "email": customer.emailid,
#             "phone": customer.phone,
#             "address": customer.address,
#             "pincode": customer.pincode,
#             "isblocked": customer.isblocked
#         }
#         return jsonify(customer_profile), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route("/api/services", methods=["GET"])
@cache.memoize(timeout=50)
@jwt_required()
@role_required(["admin", "customer"])
def get_services():
    try:
        services = Services.query.all()
        services_list = [
            {
                "id": service.id,
                "services": service.services,
                "description": service.description,
                "price": service.price,
                "time": service.time
            }
            for service in services
        ]
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a single customer by ID


@app.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'emailid': customer.emailid,
        'fullname': customer.fullname,
        'phone': customer.phone,
        'address': customer.address,
        'pincode': customer.pincode,
        'isblocked': customer.isblocked
    })

# Route to update a customer


@app.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    customer = Customer.query.get_or_404(id)
    customer.emailid = data.get('emailid', customer.emailid)
    customer.password = data.get('password', customer.password)
    customer.fullname = data.get('fullname', customer.fullname)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)
    customer.pincode = data.get('pincode', customer.pincode)
    customer.isblocked = data.get('isblocked', customer.isblocked)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})


# function for getting details of single service for editing/view purpose
@app.route('/api/services/<id>', methods=["GET"])
@jwt_required()
@role_required(["admin"])
def get_service_details(id):
    try:
        service = Services.query.get(id)
        service_details = {
            "id": service.id,
            "services": service.services,
            "description": service.description,
            "price": service.price,
            "time": service.time
        }

        return jsonify(service_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/professionalblock/<id>', methods=["POST"])
@jwt_required()
@role_required(["admin"])
def block_professional(id):
    try:
        professional = Provider.query.get(id)
        professional.isblocked = not professional.isblocked
        db.session.commit()
        return jsonify({"message": "Professional blocked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/customerblock/<id>', methods=["POST"])
@jwt_required()
@role_required(["admin"])
def block_customer(id):
    try:
        customer = Customer.query.get(id)
        customer.isblocked = not customer.isblocked
        db.session.commit()
        return jsonify({"message": "Customer blocked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/api/deleteprofessional/<id>', methods=["DELETE"])
# @jwt_required()
# def delete_professional(id):
#     try:
#         professional = Provider.query.get(id)
#         db.session.delete(professional)
#         db.session.commit()
#         return jsonify({"message": "Professional deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/api/deletecustomer/<id>', methods=["DELETE"])
# @jwt_required()
# def delete_customer(id):
#     try:
#         customer = Customer.query.get(id)
#         db.session.delete(customer)
#         db.session.commit()
#         return jsonify({"message": "Customer deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/api/approveprofessional/<id>', methods=["POST"])
@jwt_required(id)
@role_required(["admin"])
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
@role_required(["admin"])
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
@role_required(["admin"])
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
        service.time = data.get('time')
        # saving new data to db
        db.session.commit()
        cache.delete_memoized(get_services)
        service_data = {
            "id": service.id,
            "services": service.services,
            "description": service.description,
            "price": service.price,
            "time": service.time
        }
        return jsonify(service_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
@role_required(["admin"])
def delete_service(service_id):
    service = Services.query.get(service_id)
    if service is None:
        return jsonify({'error': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    cache.delete_memoized(get_services)
    return jsonify({'message': 'Service deleted successfully'}), 200


@app.route('/api/services', methods=['POST'])
@jwt_required()
@role_required(["admin"])
def add_service():
    data = request.json
    service_name = data.get('service')
    description = data.get('description')
    price = data.get('price')
    time = data.get('time')

    # Check for missing data
    if not service_name or not description or not price or not time:
        return jsonify({'error': 'Missing data'}), 400

    try:
        price = int(price)
    except ValueError:
        return jsonify({'error': 'Price must be an integer'}), 400

    # Create a new service instance
    new_service = Services(services=service_name,
                           description=description, price=price, time=time)
    db.session.add(new_service)
    db.session.commit()

    # Invalidate cache for the services list
    cache.delete_memoized(get_services)

    return jsonify({'id': new_service.id, 'service': new_service.services, 'description': new_service.description, 'price': new_service.price, 'time': new_service.time}), 201


@app.route('/api/getprovidersbyservice/<int:service_id>', methods=['GET'])
@jwt_required()
def get_providers_by_service(service_id):
    selected_service = Services.query.get(service_id)
    professionals = Provider.query.filter_by(
        service_id=service_id, isblocked=False, status="Approved").all()
    if not professionals:
        return jsonify({'error': 'Service not found'}), 404

    # Create a list of dictionaries for each professional
    providers_list = [
        {
            'id': professional.id,
            'name': professional.fullname,
            'experience': professional.experience,
            'service': selected_service.services,
            'phone': professional.phone
        }
        for professional in professionals
    ]

    return jsonify(providers_list), 200


@app.route("/api/bookings", methods=["POST"])
@jwt_required()
def create_booking():
    data = request.json
    # current_date = date.today()
    provider_id = data.get('provider_id')
    customer_id = data.get('customer_id')
    service_id = data.get('service_id')
    remarks = data.get('remarks')
    booking_date = data.get('date')

    if not all([provider_id, customer_id, service_id, remarks, booking_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Assuming date comes in format 'YYYY-MM-DD'
        booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Validate that booking date is not in the past
    if booking_date < date.today():
        return jsonify({'error': 'Cannot book appointments in the past'}), 400

    new_booking = Booking(provider_id=provider_id,
                          customer_id=customer_id, service_id=service_id,
                          date=booking_date, remarks=remarks)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        'message': 'Booking created successfully',
        'booking': {
            'id': new_booking.id,
            'provider_id': new_booking.provider_id,
            'customer_id': new_booking.customer_id,
            'service_id': new_booking.service_id,
            'remarks': new_booking.remarks,
            'date': booking_date.strftime('%Y-%m-%d')
        }
    }), 201


@app.route('/api/service-requests', methods=['GET'])
@jwt_required()
def get_service_requests():
    """Get all pending service requests"""
    try:
        # Query pending bookings, ordered by most recent first

        bookings = Booking.query.filter_by(provider_id=current_user.id)\
            .order_by(desc(Booking.date))\
            .all()

        # Join with necessary tables to get customer information
        booking_list = []
        for booking in bookings:
            # You'll need to adjust this based on your User model structure
            customer = Customer.query.get(booking.customer_id)
            provider = Provider.query.get(booking.provider_id)
            booking_data = {
                'id': booking.id,
                'customer': customer.fullname,
                'phone': customer.phone,
                'address': customer.address,
                'pincode': customer.pincode,
                'date': booking.date.strftime('%Y-%m-%d'),
                'remarks': booking.remarks
            }
            booking_list.append(booking_data)

        return jsonify({
            'status': 'success',
            'data': booking_list
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/service-requests/approve/<int:booking_id>', methods=['POST'])
@jwt_required()
def approve_service(booking_id):
    """Approve a service request"""
    try:
        booking = Booking.query.get_or_404(booking_id)

        # Update booking status
        booking.status = 'approved'
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Service request approved successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/service-requests/reject/<int:booking_id>', methods=['POST'])
@jwt_required()
def reject_service(booking_id):
    """Reject a service request"""
    try:
        booking = Booking.query.get_or_404(booking_id)

        # Update booking status
        booking.status = 'rejected'
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Service request rejected successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/provider/today-services/<int:provider_id>', methods=['GET'])
@jwt_required()
def get_provider_today_services(provider_id):
    today = date.today()
    print('today', today)
    today_bookings = Booking.query.filter_by(
        date=today, provider_id=provider_id).all()
    print('today_bookings', today_bookings)
    response = []
    for booking in today_bookings:
        customer = Customer.query.get(booking.customer_id)
        print('customer', customer, booking.customer_id)
        response.append({
            'id': booking.id,
            'customer_id': booking.customer_id,
            'service_id': booking.service_id,
            'customer_name': customer.fullname,
            'phone': customer.phone,
            'location': customer.address,
            'status': booking.status
        })

    return jsonify(response), 200


@app.route('/api/close-service/<int:booking_id>', methods=['POST'])
@jwt_required()
def close_service(booking_id):
    try:
        booking = Booking.query.get_or_404(booking_id)

        # Update booking status
        booking.status = 'closed'
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Service closed successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/provider/closed-services/<int:provider_id>', methods=['GET'])
@jwt_required()
def get_provider_closed_services(provider_id):
    try:
        # Verify the provider is requesting their own services
        current_user_id = get_jwt_identity()
        if int(current_user_id) != int(provider_id):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized access'
            }), 403

        # Join with Customer table to get customer details
        closed_bookings = db.session.query(
            Booking, Customer
        ).join(
            Customer, Booking.customer_id == Customer.id
        ).filter(
            and_(
                Booking.provider_id == provider_id,
                # Show completed and rejected services
                Booking.status.in_(['completed', 'rejected'])
            )
        ).all()

        # Format the response
        services_list = []
        for booking, customer in closed_bookings:
            services_list.append({
                'id': booking.id,
                'customerName': f"{customer.fullname}",
                'phone': customer.phone,
                'location': customer.location,
                'date': booking.date.strftime('%Y-%m-%d %H:%M:%S'),
                'status': booking.status,
                'rating': booking.rating if hasattr(booking, 'rating') else None
            })

        return jsonify({
            'status': 'success',
            'data': services_list
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/service-history/<int:customer_id>', methods=['GET'])
@jwt_required()
def service_history(customer_id):
    bookings = Booking.query.filter_by(customer_id=customer_id).all()
    
    response = []
    for booking in bookings:
        professional = Provider.query.get(booking.provider_id)
        response.append({
            'id': booking.id,
            'professional_id': booking.provider_id,
            'service_id': booking.service_id,
            'professional_name': professional.fullname,
            'date': booking.date.strftime('%Y-%m-%d'),
            'status': booking.status
        })

    return jsonify(response), 200



@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run()

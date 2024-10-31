from database import db


class user(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)


class Provider(db.Model):
    __tablename__ = 'provider'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailid = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True)
    fullname = db.Column(db.String, nullable=False)
    services = db.Column(db.String, nullable=False)
    # file = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=True)


class Customer(db.Model):
    __tablename__ = 'customer'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailid = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)


class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    services = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime)
    description = db.Column(db.String, nullable=False)

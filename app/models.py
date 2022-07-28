from app import db
from passlib.hash import pbkdf2_sha256 as hash
from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), default="default_profile.jpg")
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=False)
    address = db.Column(db.String(200))
    contact_number = db.Column(db.String(11))
    password = db.Column(db.String(250), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = hash.hash(password)

    def check_password(self, password):
        return hash.verify(password, self.password)

    def __repr__(self):
        return f"<User id:{self.id} email:{self.email}"


class Pet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), default="images/default_profile.png")
    # description = db.Column(db.String(500), nullable=True)
    name = db.Column(db.String(65), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    previous_owners = db.relationship("User", backref="pet")
    pictures = db.relationship("Images", backref="pet")
    tricks = db.relationship("Tricks", backref="pet")

    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def __repr__(self):
        return f"<Pet {self.id} {self.name} {self.breed}"


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)


class Tricks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    detail = db.Column(db.String(200))
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)

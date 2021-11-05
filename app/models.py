from app import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Nodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(32))
    name = db.Column(db.String(16))
    ip = db.Column(db.String(15))
    login = db.Column(db.String(16))
    password = db.Column(db.String(32))

@lm.user_loader
def load_user(id):
    return Admin.query.get(id)
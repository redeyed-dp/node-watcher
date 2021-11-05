from app import db

class Nodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(32))
    name = db.Column(db.String(16))
    ip = db.Column(db.String(15))
    login = db.Column(db.String(16))
    password = db.Column(db.String(32))
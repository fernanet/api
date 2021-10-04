from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """ Modelo usuário """

    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nomeusuario = db.Column(db.String(15), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)

import secrets
from datetime import datetime
from flask_bcrypt import Bcrypt

from app import db, app
from app.models import measurement

bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tuple(db.UniqueConstraint('username'))

    def __repr__(self):
        return self.id
    
    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'measurements': measurement.find_metas(self.id)
        }


def find(id):
    res = User.query.filter_by(id=id).first()
    return res.get_json() if res else None


def find_by_token(token):
    res = User.query.filter_by(token=token).first()
    return res.get_json() if res else None


def get():
    users = User.query.order_by(User.created_at).all()
    return [user.get_json() for user in users]


def create(username, password):
    token = secrets.token_hex(20)
    user = User(
        username=username,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        token=token
    )
    try:
        db.session.add(user)
        db.session.commit()
        user_json = user.get_json()
        user_json['token'] = token
        return user_json
    except:
        return None


def authenticate(username, password):
    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        return None
    user_json = found_user.get_json()
    user_json['token'] = found_user.token
    if bcrypt.check_password_hash(found_user.password, password.encode('utf-8')):
        return user_json
    else:
        return None
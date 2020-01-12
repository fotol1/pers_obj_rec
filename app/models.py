from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    interactions = db.relationship('Interaction', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % (self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    interactions = db.relationship('Interaction', backref='item', lazy='dynamic')

    def __repr__(self):
        return '<Item %r>' % (self.name)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'User id : {}, Item id : {}'.format(self.user_id, self.item_id)

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index= True, unique = True)

class Items_in_Provider(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    valid_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime, index=True)


class Score(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    score = db.Column(db.Float)

    def __repr__(self):
        return 'Pair (user {},item {}) has a score {}'.format(self.user_id,
        self.item_id,self.score)

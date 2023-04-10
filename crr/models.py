from crr import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    userrole = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    reports = db.relationship('Report', backref='author', lazy=True)
    prescribes = db.relationship('Prescribes', backref='author', lazy=True)
    products = db.relationship('Product', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Report('{self.title}', '{self.date_posted}')"


class Prescribes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(100), nullable=False)
    breakfast = db.Column(db.String(100), nullable=False, default=datetime.utcnow)
    lunch = db.Column(db.String(100), nullable=True)
    dinner = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.Integer, unique=False)
    quantity = db.Column(db.Integer, unique=False)
    price = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Prescribes('{self.title}', '{self.date_posted}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    composition = db.Column(db.String(120), unique=True, nullable=False)
    bdate = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    edate = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def is_time_slot_available(cls, time_slot):
        appointments = cls.query.filter_by(time_slot=time_slot).all()
        return len(appointments) == 0

    def __repr__(self):
        return f'<Appointment {self.id}>'
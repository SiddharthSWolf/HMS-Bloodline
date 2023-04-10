from crr import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    report = db.relationship('Report', backref='author', lazy = True)
    prescribe = db.relationship('Prescribes', backref='author', lazy = True)

    def get_reset_token(self, expires_sec = 1800):
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

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    department = db.Column(db.String(120), unique = True, nullable = False)
    speciality = db.Column(db.String(120), unique = True, nullable = False)
    date_of_joining = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    education = db.Column(db.String(20), unique = False, nullable = False)
    blood_type = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def get_reset_token(self, expires_sec = 1800):
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

class Resident(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    department = db.Column(db.String(120), unique = True, nullable = False)
    speciality = db.Column(db.String(120), unique = True, nullable = False)
    date_of_joining = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    education = db.Column(db.String(20), unique = False, nullable = False)
    blood_type = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def get_reset_token(self, expires_sec = 1800):
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

class Nurse(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    department = db.Column(db.String(120), unique = True, nullable = False)
    speciality = db.Column(db.String(120), unique = True, nullable = False)
    date_of_joining = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    education = db.Column(db.String(20), unique = False, nullable = False)
    blood_typre = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def get_reset_token(self, expires_sec = 1800):
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

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    department = db.Column(db.String(120), unique = True, nullable = False)
    speciality = db.Column(db.String(120), unique = True, nullable = False)
    date_of_joining = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    education = db.Column(db.String(20), unique = False, nullable = False)
    blood_type = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def get_reset_token(self, expires_sec = 1800):
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

class Administration(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    userrole = db.Column(db.String(20), unique = False, nullable = False)
    department = db.Column(db.String(120), unique = True, nullable = False)
    speciality = db.Column(db.String(120), unique = True, nullable = False)
    date_of_joining = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    education = db.Column(db.String(20), unique = False, nullable = False)
    blood_type = db.Column(db.String(20), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = True, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def get_reset_token(self, expires_sec = 1800):
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

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    carton_no = db.Column(db.Integer, nullable = True)
    name = db.Column(db.String(100), nullable = False)
    manufactured_by = db.Column(db.String(100), nullable = False)
    manufactured_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    chemical_comp = db.Column(db.String(100), nullable = False)
    dosage = db.Column(db.Integer, nullable = True)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Report('{self.title}', '{self.date_posted}')"

class Prescribes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    reference_id = db.Column(db.Integer, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f"Prescribes('{self.title}', '{self.date_posted}')"
    
class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    reference_id = db.Column(db.Integer, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f"Appointments('{self.title}', '{self.date_posted}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True, nullable = False)
    name = db.Column(db.String(80),unique = True, nullable = False)
    composition = db.Column(db.String(120),unique = True, nullable = False)
    bdate = db.Column(db.DateTime, unique = False, nullable = False, default = datetime.utcnow)
    edate = db.Column(db.DateTime, unique = False, nullable = False, default = datetime.utcnow)
    quantity = db.Column(db.Integer, unique = False, nullable = False)
    price = db.Column(db.Float, unique = False, nullable = False)

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
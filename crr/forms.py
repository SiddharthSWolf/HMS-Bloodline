from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired,Length, Email,EqualTo, ValidationError
from crr.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a different one.')

    def validate_email(self,email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('An account already exists with that Email.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is taken. Please choose a different one.')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('An account already exists with that Email.')


class ProductForm(FlaskForm):
    id = StringField('ID', validators = [DataRequired()])
    name = StringField('Name', validators = [DataRequired()])
    composition = StringField('Composition', validators = [DataRequired()])
    edate = DateTimeField('Expiry Date', validators = [DataRequired()])
    bdate = DateTimeField('Bought on', validators = [DataRequired()])
    quantity = StringField('Quantity in Cartons', validators = [DataRequired()])
    price = StringField('Price per Strip', validators = [DataRequired()])
    submit = SubmitField('Add Product')


class ProductUpdateForm(FlaskForm):
    id = StringField('ID', validators = [DataRequired()])
    composition = StringField('Composition', validators = [DataRequired()])
    name = StringField('Name', validators = [DataRequired()])
    edate = DateTimeField('Expiry Date', validators = [DataRequired()])
    bdate = DateTimeField('Bought on', validators = [DataRequired()])
    quantity = StringField('Quantity in Cartons', validators = [DataRequired()])
    price = StringField('Price per Strip', validators = [DataRequired()])
    submit = SubmitField('Update Product')


class ReportForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Report')
    
class PrescribesForm(FlaskForm):
    id = StringField('ID',validators=[DataRequired()])
    medication = StringField('Medication',validators=[DataRequired()])
    breakfast = StringField('Breakfast', validators = [DataRequired()])
    lunch = StringField('Lunch', validators = [DataRequired()])
    dinner = StringField('Dinner', validators = [DataRequired()])
    dosage = StringField('Dosage', validators = [DataRequired()])
    quantity = StringField('Quantity in stips', validators = [DataRequired()])
    price = StringField('Price per Strip', validators = [DataRequired()])
    submit = SubmitField('Add prescription')

class AppointmentForm(FlaskForm):
    title = StringField('Date',validators=[DataRequired()])
    submit = SubmitField('New Appointment')

class ReportUpdateForm(FlaskForm):
    title = StringField('Title')
    doctor_id = StringField('Available Agent')
    content = TextAreaField('Content')
    submit = SubmitField('Report')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', 
                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', 
                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
from flask import flash, redirect, url_for, render_template, request, abort, send_from_directory, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from crr.forms import RegistrationForm, LoginForm, UpdateAccountForm, ReportForm, ReportUpdateForm, RequestResetForm, ResetPasswordForm, PrescribesForm, AppointmentForm
from crr.models import User, Report, Prescribes, Appointments, Product
from crr import app, db, bcrypt, mail
from flask_mail import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import json

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/home")
def home():
    report = Report.query.all()
    return render_template('home.html', reports = report)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, userrole = "Patient" , email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login was Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login' , form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file= image_file, form=form)

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', product=products)

@app.route("/report/new", methods = ['GET', 'POST'])
@login_required
def new_report():
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(title = form.title.data, user_id = '404' ,content = form.content.data, author = current_user)
        db.session.add(report)
        db.session.commit()
        flash('Your report has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_report.html', title = 'New Report', form = form, legend ='New Report')

@app.route("/prescribes/new", methods = ['GET', 'POST'])
@login_required
def new_prescribes():
    form = PrescribesForm()
    if form.validate_on_submit():
        prescribes = Prescribes(title = form.title.data, user_id = '404', author = current_user)
        db.session.add(prescribes)
        db.session.commit()
        flash('Your prescribe has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_prescribes.html', title = 'New Prescribe', form = form, legend ='New Prescribe')

@app.route("/appointments/new", methods = ['GET', 'POST'])
@login_required
def new_appointments():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointments = Appointments(title = form.title.data, user_id = '404', author = current_user)
        db.session.add(appointments)
        db.session.commit()
        flash('Your appointment has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_appointment.html', title = 'New Appointment', form = form, legend ='New Appointment')

@app.route("/report/<int:report_id>")
def report(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('report.html', title = report.title, report = report)


@app.route("/report/<int:report_id>/update", methods = ['GET', 'POST'])
@login_required
def update_report(report_id):
    report = Report.query.get_or_404(report_id)
    user = User.query.get_or_404(report.user_id)
    if current_user.userrole == 'User' :
        abort(403)
    available_agent = User.query.filter_by(userrole='Agent')
    agent_list = [(i.id, i.username) for i in available_agent]
    form = ReportUpdateForm()
    form.doctor_id.choices = agent_list
    if form.validate_on_submit():
        report.title = form.title.data
        report.doctor_id = report.doctor_id
        report.content = form.content.data
        db.session.commit()
        flash('The report was updated successfully!', 'success')
        return redirect(url_for('report', report_id = report.id ))
    elif request.method == 'GET':
        form.title.data = report.title
        form.content.data = report.content
    return render_template('update_report.html', title = 'Update Agent', 
                            form = form, legend ='Update Report')



@app.route("/report/<int:report_id>/delete", methods = ['GET', 'POST'])
@login_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    if (current_user.userrole == 'User'):
        abort(403)
    db.session.delete(report)
    db.session.commit()
    flash('Your report has been deleted!', 'success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    message = Mail(
    from_email='ilamvazhuthi.j@gmail.com',
    to_emails= user.email,
    subject='Password Reset Request',
    html_content=f'''To reset your password, visit the following link:
    {url_for('reset_token', token = token, _external = True)}

    If you did not make this request then simply ignore ths email and no changes will be made 
    ''')
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

@app.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)
    
@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now login!','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)


#room hezky
@app.route('/rooms.json', methods=['GET', 'POST', 'PUT'])
def get_rooms():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'rooms', 'rooms.json')
    if request.method == 'PUT' or request.method == 'POST':
        data = request.get_json()
        if os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump(data, f)
            return jsonify({'message': 'Rooms updated successfully'})
        else:
            return jsonify({'message': 'JSON file not found'})
    else:
        return send_from_directory(os.path.dirname(json_path), os.path.basename(json_path))


@app.route('/rooms', methods=['GET', 'POST', 'PUT'])
def update_rooms():
    if request.method == 'PUT' or request.method == 'POST':
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'rooms', 'rooms.json')
        data = request.get_json()
        if os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump(data, f)
            return jsonify({'message': 'Rooms updated successfully'})
        else:
            return jsonify({'message': 'JSON file not found'})
        
    return render_template('/rooms/rooms.html')

    from flask import Flask, render_template

#map hezky
'''
@app.route('/map')
def map():
    person_json_path = os.path.join(app.root_path, 'templates', 'maps', 'person.json')
    people_json_path = os.path.join(app.root_path, 'templates', 'maps', 'people.json')
    person_data = send_from_directory(os.path.dirname(person_json_path), os.path.basename(person_json_path))
    people_data = send_from_directory(os.path.dirname(people_json_path), os.path.basename(people_json_path))
    return render_template('map.html', person_data=person_data, people_data=people_data)
'''
@app.route('/places.json')
def places():
    return send_from_directory(os.path.join(app.root_path, 'templates/maps'), 'places.json')

@app.route('/people.json')
def people():
    return send_from_directory(os.path.join(app.root_path, 'templates/maps'), 'people.json')

@app.route('/map')
def map():
    return render_template('maps/map.html')


if __name__ == '__main__':
    app.run(debug=True)

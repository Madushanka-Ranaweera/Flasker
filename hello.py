from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#add database
#old sqlite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# my new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Madushanka071@localhost/our_users'
app.config['SECRET_KEY'] = 'Madushanka'
# initialize the database
db = SQLAlchemy(app)
#create the model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Name {self.name}'

# create a form class
class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('Form submitted successfully')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/')
def index():
    first_name = 'madushanka      ranaweera'
    staff = 'This is <strong> Bold </strong>'
    pizza = ['McDonlds','pizzahut','vito']
    return render_template('index.html',first_name=first_name, staff=staff,pizza=pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully')
    return render_template('name.html', name=name, form= form)


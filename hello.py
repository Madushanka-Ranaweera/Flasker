from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Madushanka'
# create a form class
class NamerForm(FlaskForm):
    name = StringField('What is your name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('name.html', name=name, form= form)


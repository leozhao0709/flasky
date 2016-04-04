from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask.ext.mail import Mail
from flask_script import Manager
from flask.ext.moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'app', 'static'))

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('FLASK_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('FLASK_MAIL_PASSWORD')

app.config['SECRET_KEY'] = 'hard to guess string'

mail = Mail(app)
moment = Moment(app)

manager = Manager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session['name']
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session['name'])


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/browser')
def browser():
	user_agent = request.headers.get('User-Agent')
	return "<p>Your browser is %s</p>" % user_agent


class NameForm(Form):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')


if __name__ == '__main__':
	# app.run(debug=True)
	manager.run()

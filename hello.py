from flask import Flask
from flask import request
from flask.ext.mail import Mail
from flask_script import Manager
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('FLASK_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('FLASK_MAIL_PASSWORD')

mail = Mail(app)

manager = Manager(app)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/user/<name>/age/<int:id>')
def age(name, id):
    return '<h1>Hello, %s, your age is %s!</h1>' % (name, id)

@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    return "<p>Your browser is %s</p>" % user_agent


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

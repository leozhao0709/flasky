# -*- coding: utf-8 -*-

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '6:33 PM'

from flask import render_template, redirect, request, url_for, flash, session, current_app
from . import auth
from flask.ext.login import login_user, login_required, logout_user, current_user
from app.models import User
from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from app import db
from app.email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			if form.remember_me.data:
				session.permanent = True
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password', 'flashMessage_error')
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm your account', 'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email')
		return redirect(url_for('main.index'))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	return render_template('auth/register.html', form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your accounts. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.', 'flashMessage_error')
	return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account',
			   'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))


@auth.route("/resetpasswordrequest", methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Reset Your Password', 'auth/email/reset_password', user=user, token=token,
					   next=request.args.get('next'))
			flash('An email with instructions to reset your password has been sent to you.')
			return redirect(url_for('auth.login'))
		else:
			flash("The user email doesn't exist! ", 'flashMessage_error')
			return redirect(url_for('auth.password_reset_request'))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))

	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except:
		flash('The reset link is invalid or has expired.', 'flashMessage_error')
		return redirect(url_for('main.index'))
	user_id = data.get('reset')
	user = User.query.filter_by(id=user_id).first()
	if user is None:
		flash('The reset link is invalid or has expired.', 'flashMessage_error')
		return redirect(url_for('main.index'))

	form = PasswordResetForm()
	if form.validate_on_submit():
		if user.reset_password(token, form.password.data):
			flash('Your password has been updated.')
			return redirect(url_for('auth.login'))
		else:
			flash('The reset link is invalid or has expired.', 'flashMessage_error')
			return redirect(url_for('main.index'))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	return render_template('auth/reset_password.html', form=form, email=user.email)

# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, session
from . import auth
from flask.ext.login import login_user, login_required, logout_user
from app.models import User
from .forms import LoginForm, RegistrationForm
from app import db

__author__ = 'lzhao'
__date__ = '4/10/16'
__time__ = '6:33 PM'


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
        flash('Invalid username or password')
    elif form.errors.items():
        for field, errors in form.errors.items():
            flash(field + ": " + errors[0])
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
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    elif form.errors.items():
        for field, errors in form.errors.items():
            flash(field + ": " + errors[0])
    return render_template('auth/register.html', form=form)

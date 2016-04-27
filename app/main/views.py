# -*- coding: utf-8 -*-
from app.decorators import admin_required, permission_required
from app.main.forms import EditProfileForm, EditProfileAdminForm, PostForm
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..models import User, Role, Permission, Post, Follow
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response

__author__ = 'lzhao'
__date__ = '3/27/16'
__time__ = '1:06 PM'


@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, author_id=current_user._get_current_object().id)
		db.session.add(post)
		return redirect(url_for('.index'))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	page = request.args.get('page', 1, type=int)
	show_follow = False
	if current_user.is_authenticated:
		show_follow = bool(request.cookies.get('show_follow', ''))
	if show_follow:
		query = current_user.follow_posts
	else:
		query = Post.query
	print "*********show_follow********* is %s"%request.cookies.get('show_follow', 'default')
	pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
		'FLASKY_POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	return render_template('index.html', form=form, posts=posts, show_follow=show_follow, pagination=pagination)


@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	return render_template('user.html', user=user, posts=posts)


@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated.')
		return redirect(url_for('.post', id=post.id))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	form.body.data = post.body
	return render_template('edit_post.html', form=form)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('.user', username=current_user.username))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user', username=user.username))
	elif form.errors.items():
		for field, errors in form.errors.items():
			flash(field + ": " + errors[0], 'flashMessage_error')
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html', form=form, user=user)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('.user', username=username))
	current_user.following(user)
	flash('You are now following %s.' % username)
	return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	if not current_user.is_following(user):
		flash('You are not following this user.')
		return redirect(url_for('.user', username=username))
	current_user.unfollow(user)
	flash('You are not following %s anymore.' % username)
	return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
										 error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
	return render_template('followers.html', user=user, title="Followers of", endpoint='.followers',
						   pagination=pagination, follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.follow.paginate(
		page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.follow, 'timestamp': item.timestamp}
			   for item in pagination.items]
	return render_template('followers.html', user=user, title="Followed by",
						   endpoint='.followed_by', pagination=pagination, follows=follows)


@main.route('/all')
@login_required
def show_all():
	print "2222222222222"
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_follow', '', max_age=30 * 24 * 60 * 60)
	print "*********show_all********* is %s"%request.cookies.get('show_follow', 'default')
	return resp


@main.route('/follow')
@login_required
def show_follow():
	print "11111111111"
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_follow', '1', max_age=30 * 24 * 60 * 60)
	print "*********show_follow********* is %s"%request.cookies.get('show_follow', 'default')
	return resp

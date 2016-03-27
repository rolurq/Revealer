from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user,\
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, EditProfileForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.get_user(), remember=form.remember_me.data)

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category='warning')
    return redirect(url_for('index'))


@auth.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        # remove for comfirmation sending
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/register.html', form=form)


@auth.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/user.html', user=user)


@auth.route('/edit-profile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    form = EditProfileForm(current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data or current_user.name
        current_user.username = form.username.data or current_user.username
        db.session.add(current_user)

        flash('Your profile has been updated', category="success")
        return redirect(url_for('index'))
    form.name.data = current_user.name
    form.username.data = current_user.username
    return render_template('auth/edit_profile.html', form=form)

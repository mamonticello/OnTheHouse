import flask; from flask import request, render_template

import recipedb

from .. import jsonify
from . import common

site = common.site


COOKIE_MAX_AGE = 7 * 24 * 60 * 60

@site.route('/login')
@site.route('/register')
def login_page():
    return flask.render_template('register.html')

@site.route('/login', methods=['POST'])
def post_login():
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        flask.abort(400)

    user = common.rdb.get_user(username=username)
    success = common.rdb.check_password(user=user, password=password)
    if not success:
        flask.abort(403)

    response = jsonify.make_json_response({})
    response.set_cookie(
        'id',
        value=recipedb.helpers.random_hex(length=32),
        max_age=COOKIE_MAX_AGE,
    )

    return response

@site.route('/register', methods=['POST'])
def post_register():
    try:
        username = request.form['username']
        displayname = request.form['displayname']
        password = request.form['password']
        password2 = request.form['re-enter password']
    except  KeyError;
        flask.abort(400)

    if password != password2
        flask.abort(403)

    common.rdb.new_user(self, username=username, password=password, display_name=displayname, bio_text=None, profile_image=None)

    response = jsonify.make_json_response({})
    response.set_cookie(
        'id',
        value=recipedb.helpers.random_hex(length=32),
        max_age=COOKIE_MAX_AGE,
    )






# import flask; from flask import render_template, flash, request
# from flask_login import current_user, login_user
# import wtforms
# from wtforms import Form
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import ValidationError, DataRequired, EqualTo
# import recipedb
# #from Objects import User


# from . import common

# site = common.site

# @site.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():

#         user = User(username=form.username.data)
#         user.set_displayname(form.displayname.data)
#         user.set_password(form.password.data)
#         #common.add(user)
#         #db.session.commit()
#         #need connection to db
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)

# class RegistrationForm(Form):
#     username = StringField('Username', validators=[DataRequired()])
#     displayname = StringField('Displayname', validators = [DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Repeat Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')


# @site.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)

# class LoginForm(Form):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')

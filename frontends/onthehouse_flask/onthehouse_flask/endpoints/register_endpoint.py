import flask; from flask import request, render_template

import recipedb

from .. import jsonify
from . import common

site = common.site


@site.route('/login')
@site.route('/register')
def login_page():
    return flask.render_template('register.html', session_user=common.get_session(request))

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

    response = jsonify.make_json_response({'username': user.username})
    cookie_value = recipedb.helpers.random_hex(length=32)
    response.set_cookie(
        common.COOKIE_NAME,
        value=cookie_value,
        max_age=common.COOKIE_MAX_AGE,
    )
    common.new_user_cookie(cookie_value, user)

    return response

@site.route('/register', methods=['POST'])
def post_register():
    try:
        username = request.form['username']
        displayname = request.form['displayname']
        password = request.form['password']
        password2 = request.form['re-enter password']
    except KeyError:
        flask.abort(400)

    if password != password2 or username == "":
        flask.abort(403)

    user = common.rdb.new_user(
        username=username,
        password=password,
        display_name=displayname,
        bio_text=None,
        profile_image=None,
    )

    response = jsonify.make_json_response({'username': user.username})

    cookie_value = recipedb.helpers.random_hex(length=32)
    response.set_cookie(
        common.COOKIE_NAME,
        value=cookie_value,
        max_age=common.COOKIE_MAX_AGE,
    )
    common.new_user_cookie(cookie_value, user)

    return response

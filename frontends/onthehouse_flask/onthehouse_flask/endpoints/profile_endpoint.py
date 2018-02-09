from flask import request, render_template

from . import common

site = common.site


@site.route('/user/<profileid>')
def get_user(profileid):
    user = common.rdb.get_user(profileid)
    recipes = common.rdb.search(user)
    profileimg = common.rdb.get_image(user.ProfileImageID)
    response = render_template("profile.html", user=user, recipes=recipes, profileimg = profileimg)
    return response


@site.route('/user')
def user():
    response = render_template("profile-test.html")
    return response

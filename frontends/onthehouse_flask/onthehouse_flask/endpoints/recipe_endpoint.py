from flask import request, render_template

from . import common

site = common.site


@site.route('/recipe/<recipeid>')
def recipe(recipeid):
    recipe = common.rdb.get_recipe(recipeid)
    response = render_template("recipe.html", recipe=recipe)
    return response

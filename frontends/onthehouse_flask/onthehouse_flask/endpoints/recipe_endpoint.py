from flask import request, render_template

from . import common

site = common.site


@site.route('/recipe/<recipeid>')
@site.route('/recipe/<recipeid>/<slug>')
def get_recipe(recipeid, slug=None):
    recipe = common.rdb.get_recipe(recipeid)
    response = render_template("recipe.html", recipe=recipe)
    return response


@site.route('/recipe')
def recipes():
    recipes = common.rdb.get_recipes()
    response = render_template("recipes.html", recipes=recipes)
    return response

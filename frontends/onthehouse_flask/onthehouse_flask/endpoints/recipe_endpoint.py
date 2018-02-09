from flask import request, render_template

from . import common

site = common.site


@site.route('/recipe/<recipeid>')
def get_recipe(recipeid):
    recipe = common.rdb.get_recipe(recipeid)
    response = render_template("recipe.html", recipe=recipe)
    return response


@site.route('/recipe')
def recipes():
    recipes = common.rdb.get_recipes()
    response = render_template("recipes.html", recipes=recipes)
    return response


@site.route('/recipe/search')
def recipes_search():
    ingredients = request.args.get('ingredients', None)
    if ingredients is not None:
        ingredients = ingredients.split('+')
        ingredients = [common.rdb.get_ingredient(name=ing) for ing in ingredients]
    results = common.rdb.search(ingredients=ingredients)
    response = render_template("recipes.html", results=results)
    return response

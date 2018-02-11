from flask import request, render_template

import recipedb

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


@site.route('/recipe/search')
def recipes_search():
    ingredients = request.args.get('ingredients', None)

    failure = False
    if ingredients is not None:
        ingredients = ingredients.split(',')
        ingredients = [ingredient.strip() for ingredient in ingredients]
        ingredients = [ingredient for ingredient in ingredients if ingredient != '']
        final_ingredients = []
        for ingredient in ingredients:
            try:
                final_ingredients.append(common.rdb.get_ingredient(name=ingredient))
            except recipedb.exceptions.NoSuchIngredient:
                pass
        ingredients = final_ingredients
        failure = len(ingredients) == 0

    if failure:
        results = []
    else:
        results = common.rdb.search(ingredients=ingredients)
    response = render_template("recipes.html", recipes=results)
    return response

from flask import request, render_template

import recipedb

from . import common

site = common.site


def normalize_ingredients(text):
    if text is None:
        return None

    ingredients = text.split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    ingredients = [ingredient for ingredient in ingredients if ingredient != '']
    final_ingredients = []
    for ingredient in ingredients:
        try:
            final_ingredients.append(common.rdb.get_ingredient(name=ingredient))
        except recipedb.exceptions.NoSuchIngredient:
            pass

    return final_ingredients


@site.route('/recipe/<recipeid>')
@site.route('/recipe/<recipeid>/<slug>')
def get_recipe(recipeid, slug=None):
    recipe = common.rdb.get_recipe(recipeid)
    response = render_template("recipe.html", recipe=recipe, session_user=common.get_session(request))
    return response


@site.route('/recipe')
def recipes():
    recipes = common.rdb.get_recipes()
    response = render_template("recipes.html", recipes=recipes, session_user=common.get_session(request))
    return response


@site.route('/recipe/search')
def recipes_search():
    ingredients = request.args.get('ingredients', None)
    ingredients_exclude = request.args.get('exclude', None)
    meal_type = request.args.get('meal_type', None)
    strict_ingredients = request.args.get('strict', False)
    strict_ingredients = recipedb.helpers.truthystring(strict_ingredients)

    results = common.rdb.search(
        ingredients=ingredients,
        ingredients_exclude=ingredients_exclude,
        meal_type=meal_type,
        strict_ingredients=strict_ingredients,
    )

    response = render_template("recipes.html", recipes=results, session_user=common.get_session(request))
    return response

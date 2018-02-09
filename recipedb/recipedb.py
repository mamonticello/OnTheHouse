import bcrypt
import copy
import json
import logging
import os
import sqlite3
import tempfile
import shutil

from . import constants
from . import exceptions
from . import helpers
from . import objects

from voussoirkit import pathclass
from voussoirkit import sqlhelpers


logging.basicConfig()


class RecipeDB:
    def __init__(
            self,
            data_directory=None,
        ):
        super().__init__()

        if data_directory is None:
            data_directory = constants.DEFAULT_DATADIR

        # DATA DIR PREP
        data_directory = helpers.remove_path_badchars(data_directory, allowed=':/\\')
        self.data_directory = pathclass.Path(data_directory)
        os.makedirs(self.data_directory.absolute_path, exist_ok=True)

        self.log = logging.getLogger('recipedb:%s' % self.data_directory.absolute_path)
        self.log.setLevel(logging.DEBUG)

        # DATABASE
        self.database_filepath = self.data_directory.with_child(constants.DEFAULT_DBNAME)

        existing_database = self.database_filepath.exists
        self.sql = sqlite3.connect(self.database_filepath.absolute_path)

        if not existing_database:
            self._first_time_setup()

        if existing_database:
            self._check_version()

        # CONFIG
        self.config_filepath = self.data_directory.with_child(constants.DEFAULT_CONFIGNAME)
        self.config = self._load_config()
        self.log.setLevel(self.config['log_level'])

        # IMAGE DIRECTORY
        self.image_directory = self.data_directory.with_child(constants.DEFAULT_IMAGEDIR)
        os.makedirs(self.image_directory.absolute_path, exist_ok=True)

        self.on_commit_queue = []

    def _check_version(self):
        '''
        This method is run on every init except the first time.
        Raises DatabaseOutOfDate if the user's database version is behind.
        '''
        cur = self.sql.cursor()

        cur.execute('PRAGMA user_version')
        existing_version = cur.fetchone()[0]
        if existing_version != constants.DATABASE_VERSION:
            exc = exceptions.DatabaseOutOfDate(
                current=existing_version,
                new=constants.DATABASE_VERSION,
            )           
            raise exc

    def _first_time_setup(self):
        '''
        This method is run when the database is being created for the first
        time.
        '''
        self.log.debug('Performing first-time setup')

        cur = self.sql.cursor()
        statements = constants.DB_INIT.split(';')
        for statement in statements:
            cur.execute(statement)
        self.sql.commit()

    def _load_config(self):
        config = copy.deepcopy(constants.DEFAULT_CONFIGURATION)
        user_config_exists = self.config_filepath.is_file and self.config_filepath.size > 0
        if user_config_exists:
            with open(self.config_filepath.absolute_path, 'r') as handle:
                user_config = json.load(handle)
            my_keys = helpers.recursive_dict_keys(config)
            stored_keys = helpers.recursive_dict_keys(user_config)
            needs_dump = not my_keys.issubset(stored_keys)
            helpers.recursive_dict_update(config, user_config)
        else:
            needs_dump = True

        if (not user_config_exists) or needs_dump:
            with open(self.config_filepath.absolute_path, 'w') as handle:
                handle.write(json.dumps(config, indent=4, sort_keys=True))
        return config

    def _normalize_ingredient(self, ingredient):
        '''
        Try to convert the given input to a QuantitiedIngredient.
        '''
        if isinstance(ingredient, objects.QuantitiedIngredient):
            return ingredient

        if isinstance(ingredient, (tuple, list)):
            (ingredient, quantity) = ingredient
        else:
            quantity = None

        if isinstance(ingredient, str):
            ingredient = self.get_or_create_ingredient(name=ingredient)

        if isinstance(ingredient, objects.Ingredient):
            ingredient = objects.QuantitiedIngredient(ingredient=ingredient, quantity=quantity)

        if not isinstance(ingredient, objects.QuantitiedIngredient):
            raise TypeError('Type not recognized', ingredient)

        return ingredient

    def get_image(self, id):
        '''
        Fetch an image by its ID
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Image WHERE ImageID = ?', [id])
        image_row = cur.fetchone()
        if image_row is not None:
            image = objects.Image(self, image_row)
        else:
            raise ValueError('Image %s does not exist' % id)

        return image

    def get_or_create_ingredient(self, name):
        try:
            return self.get_ingredient(name=name)
        except exceptions.NoSuchIngredient:
            return self.new_ingredient(name)

    def get_ingredient(
            self,
            *,
            id=None,
            name=None,
        ):
        '''
        Fetch a single Ingredient by its ID or name.
        '''
        if id is None and name is None:
            raise TypeError('id and name can\'t both be None.')

        cur = self.sql.cursor()
        if id is not None:
            # fetch by ID
            cur.execute('SELECT * FROM Ingredient WHERE IngredientID = ?', [id])
            ingredient_row = cur.fetchone()
        else:
            # fetch by Name
            # make sure to check the autocorrect table first.
            cur.execute('SELECT * FROM Ingredient WHERE Name = ?', [name])
            ingredient_row = cur.fetchone()

        if ingredient_row is None:
            raise exceptions.NoSuchIngredient(id or name)

        ingredient = objects.Ingredient(self, ingredient_row)

        return ingredient

    def get_ingredient_tag(
            self,
            *,
            id=None,
            name=None,
        ):
        '''
        Fetch a single IngredientTag by its ID or name.
        '''
        if id is None and name is None:
            raise TypeError('id and name can\'t both be None.')

        cur = self.sql.cursor()
        if id is not None:
            # fetch by ID
            pass
        else:
            # fetch by Name
            pass

        raise NotImplementedError

    def get_recipe(self, id):
        '''
        Fetch a single Recipe by its ID.
        '''
        # SQL SELECT query and use row to construct Recipe object.
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Recipe WHERE RecipeID =?', [id])
        recipe_row = cur.fetchone()
        if recipe_row is not None:
            recipe = objects.Recipe(self, recipe_row)
        else:
            raise ValueError('Recipe %s does not exist' % id)

        return recipe

    def get_recipes(self):
        '''
        Returns all recipes
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Recipe')
        recipe_rows = cur.fetchall()
        recipe_objects = [objects.Recipe(self, row) for row in recipe_rows]
        return recipe_objects

    def new_image(self, filepath):
        '''
        Register a new image in the database.
        '''
        #generate id and generate new filepath based on id
        id = helpers.random_hex()
        filetype = filepath.rsplit('.',1)[1]
        new_filepath = '\\'.join(id[i:i+4] for i in range(0, len(id), 4)) + '.' + filetype
        shutil.copyfile(filepath,new_filepath)
        data = {
            'ImageID': id,
            'ImageFilePath': new_filepath,
        }

        (qmarks,bindings) = sqlhelpers.insert_filler(constants.SQL_IMAGE_COLUMNS, data)
        query = 'INSERT INTO Image VALUES(%s)'%qmarks
        cur = self.sql.cursor()
        cur.execute(query,bindings)
        self.sql.commit()
        image = objects.Image(self, data)
        self.log.debug('Created image with ID: %s, filepath: %s' % (image.id,image.file_path))
        return image

    def new_ingredient(self, name):
        '''
        Add a new Ingredient to the database.
        '''
        # Check if this name is already taken by the autocorrect or other ing.
        # - if so, raise an exception.
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Ingredient WHERE name = ?', [name])
        ingredient_row = cur.fetchone()
        if ingredient_row is not None:
            raise ValueError('Ingredient %s already exists' % name)

        data = {
            'IngredientID': helpers.random_hex(),
            'Name': name,
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENT_COLUMNS, data)
        query = 'INSERT INTO Ingredient VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.sql.commit()

        ingredient = objects.Ingredient(self, data)
        self.log.debug('Created ingredient %s', ingredient.name)
        return ingredient

    def new_ingredient_tag(self, name, parent=None):
        '''
        Create a new IngredientTag, either a root or grouped under `parent`.
        '''
        raise NotImplementedError

    def new_recipe(
            self,
            *,
            author: objects.User,
            blurb: str,
            country_of_origin: str,
            cuisine: str,
            ingredients: list,
            instructions: str,
            meal_type: str,
            name: str,
            prep_time: int,
            serving_size: int,
            recipe_image: objects.Image,
        ):
        '''
        Add a new recipe to the database.

        author: May be a string representing the author's ID, or a User object.
        ingredients: A list of either ingredient's ID, or Ingredient objects.
        '''
        cur = self.sql.cursor()

        recipe_id = helpers.random_hex()
        # check if `author` is string and call get_user
        author_id = None

        recipe_data = {
            'RecipeID': recipe_id,
            'Name': name,
            'AuthorID': author_id,
            'CountryOfOrigin': country_of_origin,
            'MealType': meal_type,
            'Cuisine': cuisine,
            'PrepTime': prep_time,
            'DateAdded': helpers.now(),
            'DateModified': helpers.now(),
            'Blurb': blurb,
            'ServingSize': serving_size,
            'Instructions': instructions,
            'RecipeImageID': recipe_image.id,
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_RECIPE_COLUMNS, recipe_data)
        query = 'INSERT INTO Recipe VALUES(%s)' % qmarks
        cur.execute(query, bindings)

        ingredients = [self._normalize_ingredient(ingredient) for ingredient in ingredients]

        for ingredient in ingredients:
            recipe_ingredient_data = {
                'RecipeID': recipe_id,
                'IngredientID': ingredient.id,
                'IngredientQuantity': ingredient.quantity,
                'IngredientPrefix': ingredient.prefix,
                'IngredientSuffix': ingredient.suffix,
            }
            (qmarks, bindings) = sqlhelpers.insert_filler(
                constants.SQL_RECIPEINGREDIENT_COLUMNS,
                recipe_ingredient_data
            )
            query = 'INSERT INTO Recipe_Ingredient_Map VALUES(%s)' % qmarks
            cur.execute(query, bindings)

        self.sql.commit()

        recipe = objects.Recipe(self, recipe_data)
        self.log.debug('Created recipe %s', recipe.name)
        return recipe

    def search(
            self,
            *,
            author=None,
            country=None,
            cuisine=None,
            ingredients=None,
            ingredients_exclude=None,
            limit=None,
            meal_type=None,
            name=None,
            rating=None,
        ):
        '''
        '''
        cur = self.sql.cursor()

        wheres = []

        if wheres:
            wheres = ' AND '.join(wheres)
            wheres = 'WHERE ' + wheres
        else:
            wheres = ''

        query = 'SELECT * FROM Recipe {wheres}'
        query = query.format(wheres=wheres)

        cur.execute(query)
        while True:
            recipe_row = cur.fetchone()
            if recipe_row is None:
                break
            recipe = objects.Recipe(self, recipe_row)
            # TESTS
            results.append(recipe)

        return results
    
    def new_user(
            self,
            *,
            username: str,
            display_name: str,
            password: str,
            bio_text: str
            profile_image: objects.Image
        ):
        '''
        Register a new User to the database
        '''
        cur = self.sql.cursor()

        user_id = helpers.random_hex()
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        date_joined = helpers.now()
        profile_image_id = profile_image.id
        profile_pic = profile_image.file_path

        user_data = {
            'UserID': user_id,
            'Username': username,
            'DisplayName': display_name,
            'PasswordHash': password_hash,
            'DateJoined': date_joined
            'ProfileImageID': profile_image_id
            'ProfilePic': profile_pic
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_USER_COLUMNS, user_data)
        query = 'INSERT INTO User VALUES(%s)' % qmarks
        cur.execute(query, bindings)

        self.sql.commit()

        user = objects.User(self, user_data)
        self.log.debug('Created user %s',user.username)
        return user
    
    def get_user(self, id):
        '''
        Fetch an user by their ID
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM User WHERE UserID = ?', [id])
        user_row = cur.fetchone()
        if user_row is not None:
            user = objects.User(self, user_row)
        else:
            raise ValueError('User %s does not exist' % id)

        return user

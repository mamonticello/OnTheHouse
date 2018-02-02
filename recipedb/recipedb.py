import copy
import json
import logging
import os
import sqlite3
import tempfile

from . import constants
from . import exceptions
from . import helpers
from . import objects

from voussoirkit import pathclass


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

        if id is not None:
            # fetch by ID
            pass
        else:
            # fetch by Name
            # make sure to check the autocorrect table first.
            pass

        ingredient = NotImplemented
        return ingredient

    def get_recipe(self, id):
        '''
        Fetch a single Recipe by its ID.
        '''
        # SQL SELECT query and use row to construct Recipe object.
        recipe = NotImplemented
        return recipe

    def new_ingredient(self, name):
        '''
        Add a new Ingredient to the database.
        '''
        # Check if this name is already taken by the autocorrect or other ing.
        # - if so, raise an exception.
        # INSERT statement
        ingredient = NotImplemented
        return ingredient

    def new_recipe(
            self,
            *,
            author: objects.User,
            blurb: str,
            country_of_origin: str,
            ingredients: list,
            instructions: str,
            meal_type: str,
            name: str,
            prep_time: int,
            serving_size: int,
        ):
        '''
        Add a new recipe to the database.

        author: May be a string representing the author's ID, or a User object.
        ingredients: A list of either ingredient's ID, or Ingredient objects.
        '''
        # check if `author` is string and call get_user
        # loop through ingredients, check if string and call get_ingredient
        # - if an ingredient doesn't exist, create it.
        # automatically generate random ID, current timestamp.
        # Execute INSERT statement
        # return the new Recipe object
        recipe = NotImplemented
        return recipe

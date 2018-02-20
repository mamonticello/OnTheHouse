from flask_login import UserMixin

from . import constants
from . import exceptions
from . import helpers

from voussoirkit import sqlhelpers


class ObjectBase:
    def __init__(self, recipedb):
        super().__init__()
        self.recipedb = recipedb

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.recipedb == other.recipedb and
            self.id == other.id
        )

    def __format__(self, formcode):
        if formcode == 'r':
            return repr(self)
        else:
            return str(self)

    def __hash__(self):
        return hash(self.id)


class Image(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_IMAGE_COLUMNS, db_row))

        self.id = db_row['ImageID']
        self.file_path = db_row['ImageFilePath']


class Ingredient(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_INGREDIENT_COLUMNS, db_row))

        self.id = db_row['IngredientID']
        self.name = db_row['Name']

    def add_autocorrect(self, alternate_name):
        alternate_name = self.recipedb._normalize_ingredient_name(alternate_name)
        try:
            existing = self.recipedb.get_ingredient_by_name(alternate_name)
        except exceptions.NoSuchIngredient:
            pass
        else:
            raise exceptions.IngredientExists(alternate_name)
        cur = self.recipedb.sql.cursor()

        data = {
            'IngredientID': self.id,
            'AlternateName': alternate_name,
        }
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENTAUTOCORRECT_COLUMNS, data)
        query = 'INSERT INTO IngredientAutocorrect VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def add_tag(self, tag):
        if self.has_tag(tag):
            return

        cur = self.recipedb.sql.cursor()
        data = {
            'IngredientID': self.id,
            'IngredientTagID': tag.id,
        }
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENTINGREDIENTTAG_COLUMNS, data)
        query = 'INSERT INTO Ingredient_IngredientTag_Map VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def get_tags(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT IngredientTagID FROM Ingredient_IngredientTag_Map WHERE IngredientID = ?', [self.id])
        lines = cur.fetchall()
        tags = {self.recipedb.get_ingredient_tag_by_id(line[0]) for line in lines}

        return tags

    def has_tag(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute(
            'SELECT * FROM Ingredient_IngredientTag_Map WHERE IngredientID = ? AND IngredientTagID = ?',
            [self.id, tag.id]
        )
        exists = cur.fetchone()
        return bool(exists)

    def remove_tag(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute('DELETE FROM Ingredient_IngredientTag_Map WHERE IngredientID = ? AND IngredientTagId = ?',
            [self.id, tag.id]
        )
        self.recipedb.sql.commit()

    def rename(self, name):
        # Check if `name` is already taken by an other ingredient
        # or is in the autocorrect table.
        raise NotImplementedError


class IngredientTag(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_INGREDIENTTAG_COLUMNS, db_row))

        self.id = db_row['IngredientTagID']
        self.name = db_row['TagName']
        self.parent_id = db_row['ParentTagID']

    def add_child(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT ParentTagID FROM IngredientTag WHERE IngredientTagID = ?', [tag.id])
        row = cur.fetchone()[0]
        if row is not None:
            raise exceptions.AlreadyHasParent(tag=tag, parent=self)

        data = {
            'IngredientTagID': tag.id,
            'ParentTagID': self.id,
        }
        (query, bindings) = sqlhelpers.update_filler(data, where_key='IngredientTagID')
        query = 'UPDATE IngredientTag %s' % query
        cur.execute(query, bindings)
        tag.parent_id = self.id
        self.recipedb.sql.commit()

    def get_children(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM IngredientTag WHERE ParentTagID = ?', [self.id])
        rows = cur.fetchall()
        tags = set(IngredientTag(self.recipedb, row) for row in rows)
        return tags

    def get_parent(self):
        if self.parent_id is None:
            return None

        return self.recipedb.get_ingredient_tag_by_id(self.parent_id)

    def leave_parent(self):
        parent = self.get_parent()
        if parent is None:
            return

        data = {
            'ParentTagID': None,
            'IngredientTagID': self.id,
        }
        cur = self.recipedb.sql.cursor()
        (query, bindings) = sqlhelpers.update_filler(data, where_key='IngredientTagID')
        query = 'UPDATE IngredientTag %s' % query
        cur.execute(query, bindings)
        self.parent_id = None
        self.recipedb.sql.commit()

    def rename(self, name):
        # Check if `name` is already taken somewhere else.
        raise NotImplementedError


class QuantitiedIngredient(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)

        if not db_row:
            return

        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_RECIPEINGREDIENT_COLUMNS, db_row))

        self.ingredient = self.recipedb.get_ingredient(id=db_row['IngredientID'])
        self.quantity = db_row['IngredientQuantity']
        self.prefix = db_row['IngredientPrefix']
        self.suffix = db_row['IngredientSuffix']

    def __eq__(self, other):
        return isinstance(other, QuantitiedIngredient) and self._identity == other._identity

    def __hash__(self):
        return hash(self._identity)

    @property
    def _identity(self):
        return (self.ingredient.id, self.quantity, self.prefix, self.suffix)

    @classmethod
    def from_existing(cls, ingredient, *, quantity=None, prefix=None, suffix=None):
        self = cls(ingredient.recipedb, db_row=None)
        self.ingredient = ingredient
        self.quantity = quantity
        self.prefix = prefix
        self.suffix = suffix
        return self


class Recipe(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_RECIPE_COLUMNS, db_row))

        self.id = db_row['RecipeID']
        self.name = db_row['Name']
        self.slug = helpers.slugify(self.name)
        self.author_id = db_row['AuthorID']
        if self.author_id is not None:
            self.author = self.recipedb.get_user(id=self.author_id)
        else:
            self.author = None
        self.country = db_row['CountryOfOrigin']
        self.meal_type = db_row['MealType']
        self.cuisine = db_row['Cuisine']
        self.prep_time = db_row['PrepTime']
        self.date_added = db_row['DateAdded']
        self.date_mod = db_row['DateModified']
        self.blurb = db_row['Blurb']
        self.serving_size = db_row['ServingSize']
        self.instructions = db_row['Instructions']
        self.recipe_image_id = db_row['RecipeImageID']
        self.recipe_pic = self.recipedb.get_image(self.recipe_image_id)

    def get_ingredients(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Recipe_Ingredient_Map WHERE RecipeID = ?', [self.id])
        lines = cur.fetchall()
        ingredients = {QuantitiedIngredient(self.recipedb, line) for line in lines}

        return ingredients

    def get_ingredients_and_tags(self):
        everything = {qi.ingredient for qi in self.get_ingredients()}
        tags = set()
        for ingredient in everything:
            tags.update(ingredient.get_tags())
        everything.update(tags)
        while len(tags) > 0:
            tags = {tag.get_parent() for tag in tags}
            tags = {tag for tag in tags if tag is not None}
            everything.update(tags)
        return everything

    def set_recipe_pic(self, image):
        raise NotImplementedError
        self.recipe_image_id = image.id

    def edit(
            self,
            *,
            ingredients=None,
            blurb=None,
        ):
        '''
        Let's add the rest of the arguments that we want to be able to edit.
        '''
        if blurb is not None:
            self.blurb = blurb

        # if NEW_ATTRIBUTE is not None:
        #    self.ATTRIBUTE = NEW_ATTRIBUTE

        self.date_mod = helpers.now()
        # SQL UPDATE statement to apply new properties.
        raise NotImplementedError


class Review(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_REVIEW_COLUMNS, db_row))

        self.id = db_row['ReviewID']
        self.author_id = db_row['AuthorID']
        self.recipe_id = db_row['RecipeID']
        self.score = db_row['Score']
        self.text = db_row['Text']

    def edit(self, score=None, text=None):
        if score is not None:
            self.score = score

        if text is not None:
            self.text = text

        # SQL UPDATE
        raise NotImplementedError


#class User(ObjectBase):
class User(UserMixin, ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_USER_COLUMNS, db_row))

        self.id = db_row['UserID']
        self.username = db_row['Username']
        self.display_name = db_row['DisplayName']
        self.password_hash = db_row['PasswordHash']
        self.bio_text = db_row['BioText']
        self.date_joined = db_row['DateJoined']
        self.profile_image_id = db_row['ProfileImageID']
        if self.profile_image_id is not None:
            self.profile_pic = self.recipedb.get_image(self.profile_image_id)
        else:
            self.profile_pic = None

    def set_display_name(self, display_name):
        raise NotImplementedError

    def set_profile_pic(self, image):
        raise NotImplementedError
        self.profile_image_id = image.id

    def set_bio(self, bio_text):
        raise NotImplementedError

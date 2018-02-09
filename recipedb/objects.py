from . import constants

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

    def add_tag(self, tag):
        raise NotImplementedError

    def remove_tag(self, tag):
        raise NotImplementedError

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

    def __hash__(self):
        identity = (self.ingredient.id, self.quantity, self.prefix, self.suffix)
        return hash(identity)

    @classmethod
    def from_existing(cls, ingredient, *, quantity=None, prefix=None, suffix=None):
        self = cls()
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
        self.author_id = db_row['AuthorID']
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
        raise NotImplementedError

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


class User(ObjectBase):
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
        self.profile_pic = self.recipedb.get_image(self.profile_image_id)

    def set_display_name(self, display_name):
        raise NotImplementedError

    def set_profile_pic(self, image):
        raise NotImplementedError
        self.profile_image_id = image.id

    def set_bio(self, bio_text):
        raise NotImplementedError

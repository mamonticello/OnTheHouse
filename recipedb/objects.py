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
    pass

class Ingredient(ObjectBase):
    pass

class IngredientTag(ObjectBase):
    pass

class Recipe(ObjectBase):
    pass

class Review(ObjectBase):
    pass

class User(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_USER_COLUMNS, db_row))

        self.id = db_row['UserID']
        self.username = db_row['Username']
        self.display_name = db_row['DisplayName']
        self.bio_text = db_row['BioText']
        self.date_joined = db_row['DateJoined']
        self.profile_image_id = db_row['ProfileImageID']

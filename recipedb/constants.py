'''
This file contains data that is constant during runtime and shared throughout
the entire program.

This file should not import any other file in the same package.
'''

import logging


FILENAME_BADCHARS = '\\/:*?<>|"'

# Note: Setting user_version pragma in init sequence is safe because it only
# happens after the out-of-date check occurs, so no chance of accidentally
# overwriting it.
DATABASE_VERSION = 1
DB_INIT = '''
PRAGMA count_changes = OFF;
PRAGMA cache_size = 10000;
PRAGMA user_version = {user_version};

----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Image(
    ImageID TEXT PRIMARY KEY,
    ImageFilePath TEXT
);
CREATE INDEX IF NOT EXISTS index_Image_ImageID on Image(ImageID);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS User(
    UserID TEXT PRIMARY KEY,
    Username TEXT COLLATE NOCASE,
    DisplayName TEXT COLLATE NOCASE,
    BioText TEXT,
    DateJoined INT,
    PasswordHash BLOB,
    ProfileImageID TEXT,
    FOREIGN KEY(ProfileImageID) REFERENCES Image(ImageID)
);
CREATE INDEX IF NOT EXISTS index_User_UserID on User(UserID);
CREATE INDEX IF NOT EXISTS index_User_Username on User(Username COLLATE NOCASE);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Recipe(
    RecipeID TEXT PRIMARY KEY,
    Name TEXT,
    AuthorID TEXT,
    CountryOfOrigin TEXT,
    MealType TEXT,
    Cuisine TEXT,
    PrepTime INT,
    DateAdded INT,
    DateModified INT,
    Blurb TEXT,
    ServingSize INT,
    Instructions TEXT,
    FOREIGN KEY(AuthorID) REFERENCES User(UserID)
);
CREATE INDEX IF NOT EXISTS index_Recipe_RecipeID on Recipe(RecipeID);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Ingredient(
    IngredientID TEXT PRIMARY KEY,
    Name TEXT
);
CREATE INDEX IF NOT EXISTS index_Ingredient_IngredientID on Ingredient(IngredientID);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Recipe_Ingredient_Map(
    RecipeID TEXT,
    IngredientID TEXT,
    IngredientQuantity TEXT,
    IngredientPrefix TEXT,
    IngredientSuffix TEXT,
    FOREIGN KEY(RecipeID) REFERENCES Recipe(RecipeID),
    FOREIGN KEY(IngredientID) REFERENCES Ingredient(IngredientID)
);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Review(
    ReviewID TEXT PRIMARY KEY,
    AuthorID TEXT,
    RecipeID TEXT,
    Score INT,
    Text TEXT,
    FOREIGN KEY(AuthorID) REFERENCES User(UserID),
    FOREIGN KEY(RecipeID) REFERENCES Recipe(RecipeID)
);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS IngredientTag(
    IngredientTagID TEXT PRIMARY KEY,
    TagName TEXT,
    ParentTagID TEXT
);
----------------------------------------------------------------------------------------------------

'''.format(user_version=DATABASE_VERSION)

def _extract_column_names(table):
    statement = DB_INIT.split('CREATE TABLE IF NOT EXISTS %s(' % table)[1]
    statement = statement.split(');')[0]
    statement = statement.replace('\n', ' ')
    statements = statement.split(',')
    statements = [statement.strip() for statement in statements]
    columns = [statement for statement in statements if 'FOREIGN KEY' not in statement]
    columns = [column.split(' ')[0] for column in columns]
    return columns

SQL_IMAGE_COLUMNS = _extract_column_names('Image')
SQL_INGREDIENT_COLUMNS = _extract_column_names('Ingredient')
SQL_INGREDIENTTAG_COLUMNS = _extract_column_names('IngredientTag')
SQL_RECIPE_COLUMNS = _extract_column_names('Recipe')
SQL_RECIPEINGREDIENT_COLUMNS = _extract_column_names('Recipe_Ingredient_Map')
SQL_REVIEW_COLUMNS = _extract_column_names('Review')
SQL_USER_COLUMNS = _extract_column_names('User')

_sql_dictify = lambda columns: {key:index for (index, key) in enumerate(columns)}
SQL_USER = _sql_dictify(SQL_USER_COLUMNS)

DEFAULT_DATADIR = '.\\_recipedb'
DEFAULT_DBNAME = 'recipe.db'
DEFAULT_CONFIGNAME = 'config.json'
DEFAULT_IMAGEDIR = 'images'

DEFAULT_CONFIGURATION = {
    'log_level': logging.DEBUG,
}

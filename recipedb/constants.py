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
CREATE TABLE IF NOT EXISTS Image_Recipe_Map(
    RecipeID TEXT,
    ImageID TEXT,
    FOREIGN KEY(RecipeID) REFERENCES Recipe(RecipeID),
    FOREIGN KEY(ImageID) REFERENCES Image(ImageID)
);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Ingredient(
    IngredientID TEXT PRIMARY KEY,
    Name TEXT COLLATE NOCASE
);
CREATE INDEX IF NOT EXISTS index_Ingredient_IngredientID on Ingredient(IngredientID);
CREATE INDEX IF NOT EXISTS index_Ingredient_Name on Ingredient(Name COLLATE NOCASE);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS IngredientAutocorrect(
    IngredientID TEXT,
    AlternateName TEXT,
    FOREIGN KEY(IngredientID) REFERENCES Ingredient(IngredientID)
);
CREATE INDEX IF NOT EXISTS index_IngredientAutocorrect_AlternateName on IngredientAutocorrect(AlternateName);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS IngredientTag(
    IngredientTagID TEXT PRIMARY KEY,
    TagName TEXT COLLATE NOCASE,
    ParentTagID TEXT
);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Ingredient_IngredientTag_Map(
    IngredientID TEXT,
    IngredientTagID TEXT,
    FOREIGN KEY(IngredientID) REFERENCES Ingredient(IngredientID),
    FOREIGN KEY(IngredientTagID) REFERENCES IngredientTag(IngredientTagID)
);
CREATE INDEX IF NOT EXISTS index_IngredientIngredientTagMap_IngredientID on Ingredient_IngredientTag_Map(IngredientID);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Recipe(
    RecipeID TEXT PRIMARY KEY,
    Name TEXT COLLATE NOCASE,
    AuthorID TEXT,
    CountryOfOrigin TEXT COLLATE NOCASE,
    MealType TEXT COLLATE NOCASE,
    Cuisine TEXT COLLATE NOCASE,
    PrepTime INT,
    DateAdded INT,
    DateModified INT,
    Blurb TEXT,
    ServingSize INT,
    Instructions TEXT,
    RecipeImageID TEXT,
    FOREIGN KEY(RecipeImageID) REFERENCES Image(ImageID)
    FOREIGN KEY(AuthorID) REFERENCES User(UserID)
);
CREATE INDEX IF NOT EXISTS index_Recipe_RecipeID on Recipe(RecipeID);
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
CREATE INDEX IF NOT EXISTS index_RecipeIngredientMap_RecipeID on Recipe_Ingredient_Map(RecipeID);
CREATE INDEX IF NOT EXISTS index_RecipeIngredientMap_IngredientID on Recipe_Ingredient_Map(IngredientID);
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
CREATE INDEX IF NOT EXISTS index_Review_ReviewID on Review(ReviewID);
CREATE INDEX IF NOT EXISTS index_Review_AuthorID on Review(AuthorID);
CREATE INDEX IF NOT EXISTS index_Review_RecipeID on Review(RecipeID);
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
CREATE TABLE IF NOT EXISTS UserSettings(
    UserID TEXT,
    SettingName TEXT,
    SettingValue TEXT,
    FOREIGN KEY(UserID) REFERENCES User(UserID)
);
CREATE INDEX IF NOT EXISTS index_UserSettings_UserID_SettingName on UserSettings(UserID, SettingName);
----------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS User_Following_Map(
    UserID TEXT,
    TargetID TEXT,
    FOREIGN KEY(UserID) REFERENCES User(UserID),
    FOREIGN KEY(TargetID) REFERENCES User(UserID)
);
CREATE INDEX IF NOT EXISTS index_UserFollowingMap_UserID on User_Following_Map(UserID);
CREATE INDEX IF NOT EXISTS index_UserFollowingMap_TargetID on User_Following_Map(TargetID);
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
SQL_INGREDIENTAUTOCORRECT_COLUMNS = _extract_column_names('IngredientAutocorrect')
SQL_INGREDIENTTAG_COLUMNS = _extract_column_names('IngredientTag')
SQL_INGREDIENTINGREDIENTTAG_COLUMNS = _extract_column_names('Ingredient_IngredientTag_Map')
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

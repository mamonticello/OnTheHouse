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
----------------------------------------------------------------------------------------------------

'''.format(user_version=DATABASE_VERSION)

def _extract_column_names(table):
    statement = DB_INIT.split('CREATE TABLE IF NOT EXISTS %s(' % table)[1]
    statement = statement.split(');')[0]
    statement = statement.replace('\n', ' ')
    columns = statement.split(',')
    columns = [column.strip().split(' ')[0] for column in columns]
    return columns

SQL_IMAGE_COLUMNS = _extract_column_names('Image')
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

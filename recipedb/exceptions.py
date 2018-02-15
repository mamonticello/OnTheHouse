'''
This file contains custom exceptions that will be raised by the backend.
'''
import re

def pascal_to_loudsnakes(text):
    '''
    NoSuchPhoto -> NO_SUCH_PHOTO
    '''
    match = re.findall('[A-Z][a-z]*', text)
    text = '_'.join(match)
    text = text.upper()
    return text


class ErrorTypeAdder(type):
    '''
    During definition, the Exception class will automatically receive a class
    attribute called `error_type` which is just the class's name as a string
    in the loudsnake casing style. NoSuchPhoto -> NO_SUCH_PHOTO.

    This is used for serialization of the exception object and should
    basically act as a status code when displaying the error to the user.

    Thanks Unutbu
    http://stackoverflow.com/a/18126678
    '''
    def __init__(cls, name, bases, clsdict):
        type.__init__(cls, name, bases, clsdict)
        cls.error_type = pascal_to_loudsnakes(name)


class RecipeDBException(Exception, metaclass=ErrorTypeAdder):
    '''
    Base type for all of the RecipeDBException exceptions.
    Subtypes should have a class attribute `error_message`. The error message
    may contain {format} strings which will be formatted using the
    Exception's constructor arguments.
    '''
    error_message = ''
    def __init__(self, *args, **kwargs):
        self.given_args = args
        self.given_kwargs = kwargs
        self.error_message = self.error_message.format(*args, **kwargs)
        self.args = (self.error_message, args, kwargs)

    def __str__(self):
        return self.error_type + '\n' + self.error_message


OUTOFDATE = '''
Database is out of date. {current} should be {new}.
Please use utilities\\database_upgrader.py
'''.strip()
class DatabaseOutOfDate(RecipeDBException):
    '''
    Raised by RecipeDB __init__ if the user's database is behind.
    '''
    error_message = OUTOFDATE


class Exists(RecipeDBException):
    pass

class UserExists(Exists):
    error_message = 'User "{}" already exists.'


class NoSuch(RecipeDBException):
    pass

class NoSuchImage(NoSuch):
    error_message = 'Image "{}" does not exist.'

class NoSuchIngredient(NoSuch):
    error_message = 'Ingredient "{}" does not exist.'

class NoSuchIngredientTag(NoSuch):
    error_message = 'IngredientTag "{}" does not exist.'

class NoSuchRecipe(NoSuch):
    error_message = 'Recipe "{}" does not exist.'

class NoSuchReview(NoSuch):
    error_message = 'Review "{}" does not exist.'

class NoSuchUser(NoSuch):
    error_message = 'User "{}" does not exist.'

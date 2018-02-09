'''
This file contains toplevel functions that are used throughout the program
but don't belong to any one class in particular.
'''
import datetime
import math
import os
import string
import unicodedata

from . import constants
from . import exceptions


def now(timestamp=True):
    '''
    Return the current UTC timestamp or datetime object.
    '''
    n = datetime.datetime.now(datetime.timezone.utc)
    if timestamp:
        return n.timestamp()
    return n

def random_hex(length=12):
    randbytes = os.urandom(math.ceil(length / 2))
    token = ''.join('{:02x}'.format(x) for x in randbytes)
    token = token[:length]
    return token

def read_filebytes(filepath, range_min, range_max, chunk_size=2 ** 20):
    '''
    Yield chunks of bytes from the file between the endpoints.
    '''
    range_span = range_max - range_min

    #print('read span', range_min, range_max, range_span)
    f = open(filepath, 'rb')
    f.seek(range_min)
    sent_amount = 0
    with f:
        while sent_amount < range_span:
            #print(sent_amount)
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break

            yield chunk
            sent_amount += len(chunk)

def recursive_dict_update(d1, d2):
    '''
    Update d1 using d2, but when the value is a dictionary update the insides
    instead of replacing the dictionary itself.
    '''
    for (key, value) in d2.items():
        if isinstance(value, dict):
            existing = d1.get(key, None)
            if existing is None:
                d1[key] = value
            else:
                recursive_dict_update(existing, value)
        else:
            d1[key] = value

def recursive_dict_keys(d):
    '''
    Given a dictionary, return a set containing all of its keys and the keys of
    all other dictionaries that appear as values within. The subkeys will use \\
    to indicate their lineage.

    {
        'hi': {
            'ho': 'neighbor'
        }
    }

    returns

    {'hi', 'hi\\ho'}
    '''
    keys = set(d.keys())
    for (key, value) in d.items():
        if isinstance(value, dict):
            subkeys = {'%s\\%s' % (key, subkey) for subkey in recursive_dict_keys(value)}
            keys.update(subkeys)
    return keys

def remove_characters(text, characters):
    translator = {ord(c): None for c in characters}
    text = text.translate(translator)
    return text

def remove_control_characters(text):
    '''
    Thanks Alex Quinn
    https://stackoverflow.com/a/19016117

    unicodedata.category(character) returns some two-character string
    where if [0] is a C then the character is a control character.
    '''
    return ''.join(c for c in text if unicodedata.category(c)[0] != 'C')

def remove_path_badchars(filepath, allowed=''):
    '''
    Remove the bad characters seen in constants.FILENAME_BADCHARS, except
    those which you explicitly permit.

    'file*name' -> 'filename'
    ('D:\\file*name', allowed=':\\') -> 'D:\\filename'
    '''
    badchars = remove_characters(constants.FILENAME_BADCHARS, allowed)
    filepath = remove_characters(filepath, badchars)

    filepath = filepath.replace('/', os.sep)
    filepath = filepath.replace('\\', os.sep)
    return filepath

def slugify(text, maxlen=24):
    text = text.lower()
    text = text.strip().replace(' ', '-')
    allowed_chars = string.ascii_letters + string.digits + '-'
    text = ''.join(c for c in text if c in allowed_chars)
    words = text.split('-')

    if len(words) == 0:
        return ''

    while True:
        slug = '-'.join(words)
        if len(slug) > maxlen:
            if len(words) == 1:
                slug = slug[:maxlen]
                break
            else:
                words = words[:-1]
        else:
            break
    return slug

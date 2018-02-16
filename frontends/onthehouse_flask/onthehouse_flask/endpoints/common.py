import flask; from flask import request
import os
import mimetypes

import recipedb

from voussoirkit import pathclass

from .. import jsonify
from .. import jinja_filters


root_dir = pathclass.Path(__file__).parent.parent.parent

TEMPLATE_DIR = root_dir.with_child('templates')
STATIC_DIR = root_dir.with_child('static')
FAVICON_PATH = STATIC_DIR.with_child('favicon.png')

site = flask.Flask(
    __name__,
    template_folder=TEMPLATE_DIR.absolute_path,
    static_folder=STATIC_DIR.absolute_path,
)
site.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=180,
    TEMPLATES_AUTO_RELOAD=True,
)
site.jinja_env.add_extension('jinja2.ext.do')
site.jinja_env.trim_blocks = True
site.jinja_env.lstrip_blocks = True
site.jinja_env.filters['divmod'] = divmod
site.jinja_env.filters['split_paragraphs'] = jinja_filters.split_paragraphs
site.jinja_env.filters['unix_to_human'] = jinja_filters.unix_to_human
site.debug = True

rdb = recipedb.RecipeDB()

COOKIE_MAX_AGE = 7 * 24 * 60 * 60
COOKIE_NAME = 'cookie_name'
cookie_dict = {}

def back_url():
    return request.args.get('goto') or request.referrer or '/'

def new_user_cookie(cookie_value, user):
    cookie_dict[cookie_value] = user

def get_user_from_cookie(cookie_value):
    return cookie_dict.get(cookie_value, None)

def get_session(request):
    cookie_check = request.cookies.get(COOKIE_NAME, None)
    return get_user_from_cookie(cookie_check)

def send_file(filepath, override_mimetype=None):
    '''
    Range-enabled file sending.
    '''
    try:
        file_size = os.path.getsize(filepath)
    except FileNotFoundError:
        flask.abort(404)

    outgoing_headers = {}
    if override_mimetype is not None:
        mimetype = override_mimetype
    else:
        mimetype = mimetypes.guess_type(filepath)[0]

    if mimetype is not None:
        if 'text/' in mimetype:
            mimetype += '; charset=utf-8'
        outgoing_headers['Content-Type'] = mimetype

    if 'range' in request.headers:
        desired_range = request.headers['range'].lower()
        desired_range = desired_range.split('bytes=')[-1]

        int_helper = lambda x: int(x) if x.isdigit() else None
        if '-' in desired_range:
            (desired_min, desired_max) = desired_range.split('-')
            range_min = int_helper(desired_min)
            range_max = int_helper(desired_max)
        else:
            range_min = int_helper(desired_range)

        if range_min is None:
            range_min = 0
        if range_max is None:
            range_max = file_size

        # because ranges are 0-indexed
        range_max = min(range_max, file_size - 1)
        range_min = max(range_min, 0)

        range_header = 'bytes {min}-{max}/{outof}'.format(
            min=range_min,
            max=range_max,
            outof=file_size,
        )
        outgoing_headers['Content-Range'] = range_header
        status = 206
    else:
        range_max = file_size - 1
        range_min = 0
        status = 200

    outgoing_headers['Accept-Ranges'] = 'bytes'
    outgoing_headers['Content-Length'] = (range_max - range_min) + 1

    if request.method == 'HEAD':
        outgoing_data = bytes()
    else:
        outgoing_data = recipedb.helpers.read_filebytes(
            filepath,
            range_min=range_min,
            range_max=range_max,
            chunk_size=P.config['file_read_chunk'],
        )

    response = flask.Response(
        outgoing_data,
        status=status,
        headers=outgoing_headers,
    )
    return response

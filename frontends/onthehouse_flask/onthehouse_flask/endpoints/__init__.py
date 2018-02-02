import flask; from flask import request
import random

from . import common
from . import recipe_endpoint

site = common.site


@site.route('/')
def root():
    return flask.render_template('root.html')


@site.route('/favicon.ico')
@site.route('/favicon.png')
def favicon():
    return flask.send_file(common.FAVICON_PATH.absolute_path)


if __name__ == '__main__':
    #site.run(threaded=True)
    pass

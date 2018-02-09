import flask; from flask import request
from flask_login import LoginManager
import random


from . import common
from . import recipe_endpoint
from . import profile_endpoint

site = common.site
loginmanager = LoginManager(site)


@site.route('/')
def root():
    return flask.render_template('root.html')


@site.route('/img/<imgid>')
def get_img(imgid):
    img = common.rdb.get_image(imgid)
    return flask.send_file(img.file_path)


@site.route('/favicon.ico')
@site.route('/favicon.png')
def favicon():
    return flask.send_file(common.FAVICON_PATH.absolute_path)


if __name__ == '__main__':
    #site.run(threaded=True)
    pass

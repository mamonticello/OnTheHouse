import flask; from flask import request, render_template

from . import common

site = common.site


@site.route('/image/<image_id>')
@site.route('/user/<image_id>.<ext>')
def get_image(image_id, ext=None):
    image = common.rdb.get_image(id=image_id)
    return flask.send_file(image.file_path)

from . import decorators
from . import endpoints
from . import jsonify

site = endpoints.site

from flask_login import LoginManager

app = Flask(__name__)
# ...
login = LoginManager(app)

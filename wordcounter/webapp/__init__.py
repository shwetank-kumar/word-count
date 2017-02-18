from flask import Blueprint

webapp = Blueprint('webapp', __name__, template_folder='templates' )

from . import views

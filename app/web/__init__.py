from flask import Blueprint

web_blueprint = Blueprint('web', __name__)

from . import handler

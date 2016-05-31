from flask import Blueprint
from .download import DownloadScheduler

web_blueprint = Blueprint('web', __name__)
download_scheduler = DownloadScheduler()

from . import handler

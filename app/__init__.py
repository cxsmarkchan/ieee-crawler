from mongoengine import connect
from flask import Flask
import logging


# initialize logger
logger = logging.getLogger('ieee_crawler_logger')
logger.setLevel(logging.INFO)
hdr = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)
logger.addHandler(hdr)
logger.info('Logger initialized.')

connect('ieee_crawler')
logger.info('Database connected.')


def create_app():
    # flask app
    app = Flask(__name__)

    from .web import web_blueprint

    app.register_blueprint(web_blueprint)

    return app

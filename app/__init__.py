from mongoengine import connect
import logging

logger = logging.getLogger('ieee_crawler_logger')
logger.setLevel(logging.INFO)
hdr = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)
logger.addHandler(hdr)
logger.info('Logger initialized.')

connect('ieee_crawler')
logger.info('Database connected.')


from gevent.pool import Pool
from ..ieee.article import ArticleController


class DownloadScheduler(object):
    def __init__(self):
        self.__pool = Pool()

    def download(self, article_number):
        self.__pool.spawn(DownloadScheduler.__download, article_number)

    @staticmethod
    def __download(article_number):
        article = ArticleController(article_number)
        article.download()

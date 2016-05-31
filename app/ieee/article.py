import requests
from pyquery import PyQuery
from .. import logger
from ..models import Article


class ArticleController:
    def __init__(self, article):
        if isinstance(article, Article):
            self.__article = article
        else:
            self.__article = Article.objects.get(entry_number=str(article))

    def __eq__(self, other):
        return isinstance(other, ArticleController) \
                   and self.__article == other.__article

    @staticmethod
    def get_all_by_status(status):
        articles = Article.objects.filter(status=status).order_by('title')
        return [ArticleController(article) for article in articles]

    @staticmethod
    def get_brief_by_status(status):
        articles = Article.objects.filter(status=status).order_by('title')
        brief = []
        for article in articles:
            brief.append({
                'entry_number': article.entry_number,
                'title': article.title,
                'status': article.status
            })
        return brief

    @staticmethod
    def get_all_unvisited():
        return ArticleController.get_all_by_status(Article.UNVISITED)

    @staticmethod
    def get_all_unvisited_brief():
        return ArticleController.get_brief_by_status(Article.UNVISITED)

    @staticmethod
    def get_all_need_further():
        return ArticleController.get_all_by_status(Article.NEED_FURTHER)

    @staticmethod
    def get_all_need_further_brief():
        return ArticleController.get_brief_by_status(Article.NEED_FURTHER)

    @staticmethod
    def get_all_important():
        return ArticleController.get_all_by_status(Article.IMPORTANT)

    @staticmethod
    def get_all_important_brief():
        return ArticleController.get_brief_by_status(Article.IMPORTANT)

    @property
    def entry_number(self):
        return self.__article.entry_number

    @property
    def title(self):
        return self.__article.title

    @property
    def author(self):
        return self.__article.author

    @property
    def journal(self):
        return self.__article.journal

    @property
    def year(self):
        return self.__article.year

    @property
    def volume(self):
        return self.__article.volume

    @property
    def number(self):
        return self.__article.number

    @property
    def pages(self):
        return self.__article.pages

    @property
    def abstract(self):
        return self.__article.abstract

    @property
    def keyword(self):
        return self.__article.keyword

    @property
    def doi(self):
        return self.__article.doi

    @property
    def issn(self):
        return self.__article.issn

    @property
    def status(self):
        return self.__article.status

    @status.setter
    def status(self, value):
        self.__article.status = value
        self.__article.save()

    @property
    def note(self):
        return self.__article.note

    @note.setter
    def note(self, value):
        self.__article.note = value
        self.__article.save()

    @property
    def downloaded(self):
        return self.__article.downloaded

    @property
    def bibtex(self):
        return str(self.__article)

    @property
    def entry(self):
        return {
            'entry_number': self.entry_number,
            'title': self.title,
            'author': self.author,
            'journal': self.journal,
            'year': self.year,
            'volume': self.volume,
            'number': self.number,
            'pages': self.pages,
            'abstract': self.abstract,
            'keyword': self.keyword,
            'doi': self.doi,
            'issn': self.issn,
            'status': self.status,
            'note': self.note,
            'downloaded': self.downloaded
        }

    def download(self):
        frame = requests.get(
            url='http://ieeexplore.ieee.org/stamp/stamp.jsp',
            params={
                'arnumber': self.entry_number
            }
        )
        query = PyQuery(frame.text)
        url = query('frame:eq(1)').attr('src')

        logger.info('Downloading:' + url)

        r = requests.get(url)
        with open('pdf/' + self.entry_number + '.pdf', 'wb') as fid:
            fid.write(r.content)

        logger.info('Downloaded: ' + self.entry_number)

        self.__article.downloaded = True
        self.__article.save()

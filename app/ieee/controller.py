from mongoengine import DoesNotExist
import requests
from pyquery import PyQuery
from ..models import Journal


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def get_article(article_number):
        from .article import ArticleController
        return ArticleController(article_number)

    @staticmethod
    def get_journal(journal_number):
        from .journal import JournalController
        return JournalController(journal_number)

    @staticmethod
    def get_journal_object(journal_number):
        '''
        If the journal exists in database, return the object.
        Else construct the object in database, and return it.
        :param journal_number:
        :return:
        '''
        try:
            journal = Journal.objects.get(entry_number=str(journal_number))
        except DoesNotExist:
            journal = Journal()
            journal.entry_number = str(journal_number)
            url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
            payload = {
                'punumber': journal_number
            }
            r = requests.get(url, params=payload)
            query = PyQuery(r.text)
            journal.name = query('#journal-page-hdr h1').text().strip()
            journal.save()

        return journal

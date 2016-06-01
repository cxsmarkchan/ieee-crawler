import math
import time
import requests
from requests import Timeout
from pyquery import PyQuery
from mongoengine import DoesNotExist
from pymongo.errors import ServerSelectionTimeoutError
from .. import logger
from ..models import Issue, Article
from .citation import CitationLoader


class IssueController:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, issue):
        if isinstance(issue, Issue):
            self.__issue = issue
        else:
            self.__issue = Issue.objects.get(entry_number=str(issue))
        self.__journal = self.__issue.journal_reference

    def __eq__(self, other):
        return isinstance(other, IssueController) \
               and self.__issue == other.__issue

    @property
    def entry_number(self):
        return self.__issue.entry_number

    @property
    def journal_name(self):
        return self.__journal.name

    @property
    def year(self):
        return self.__issue.year

    @property
    def number(self):
        return self.__issue.number

    @property
    def status(self):
        return self.__issue.status

    def update(self):
        numbers = self.crawl_article_numbers()
        self.crawl_articles(numbers)

    def get_article_brief(self):
        articles = Article.objects.filter(issue_reference=self.__issue).order_by('title')
        brief = []
        for article in articles:
            brief.append({
                'entry_number': article.entry_number,
                'title': article.title,
                'status': article.status
            })

        return brief

    def crawl_article_numbers(self):
        journal_number = self.__journal.entry_number

        payload = {
            'punumber': journal_number
        }

        if self.__issue.status == Issue.CURRENT_ISSUE:
            url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        else:
            url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
            payload['isnumber'] = self.__issue.entry_number

        logger.info('Obtaining article numbers:' + url)

        r = None
        num_try = 1
        while True:
            try:
                logger.info('Page 1: Trying %d time(s)' % num_try)
                r = requests.get(url=url, params=payload)
                break
            except Timeout:
                num_try += 1
                if num_try > 10:
                    logger.info('Timeout')
                    break
        del num_try
        if not r:
            return []

        query = PyQuery(r.text)
        number_of_articles = self.__get_number_of_articles(query)

        numbers = []

        for i in range(0, math.ceil(number_of_articles / self.INIT_ARTICLE_PER_PAGE)):
            if i > 0:
                payload['pageNumber'] = i + 1
                r = None
                num_try = 1
                while True:
                    try:
                        logger.info('Page %d: Trying %d time(s)' % (i + 1, num_try))
                        # prevent from locked by Tsinghua library
                        time.sleep(5)
                        r = requests.get(url=url, params=payload)
                        break
                    except Timeout:
                        num_try += 1
                        if num_try > 10:
                            logger.info('Timeout')
                            break
                del num_try
                if not r:
                    continue
                query = PyQuery(r.text)

            elems = query('#results-blk .results li')

            tmp_numbers = [elem.attrib['aria-describedby'].split(' ')[0].split('-')[3]
                           for elem in elems]
            numbers.extend(tmp_numbers)

        logger.info('Article numbers obtained: %d articles' % number_of_articles)

        return numbers

    def crawl_articles(self, numbers):
        citation_loader = CitationLoader(numbers)
        entries = citation_loader.get_bibtex()
        articles = {}

        for entry in entries:
            number = entry['ID']

            try:
                article = Article.objects.get(entry_number=number)
                logger.info('Article [%s] already exists, it will be updated.' % number)
            except (DoesNotExist, ServerSelectionTimeoutError):
                article = Article()
                article.entry_number = number
                logger.info('Article [%s] is a new article.' % number)

            article.title = entry['title'] if 'title' in entry else ''
            article.author = entry['author'] if 'author' in entry else ''
            article.journal = entry['journal'] if 'journal' in entry else ''
            article.year = entry['year'] if 'year' in entry else ''
            article.volume = entry['volume'] if 'volume' in entry else ''
            article.number = entry['number'] if 'number' in entry else ''
            article.pages = entry['pages'] if 'pages' in entry else ''
            article.abstract = entry['abstract'] if 'abstract' in entry else ''
            article.keyword = entry['keyword'] if 'keyword' in entry else ''
            article.doi = entry['doi'] if 'doi' in entry else ''
            article.issn = entry['issn'] if 'issn' in entry else ''
            article.issue_reference = self.__issue

            try:
                article.save()
                logger.info('Article [%s] saved.' % number)
            except ServerSelectionTimeoutError:
                logger.info('Cannot connect to database, Article [%s] will not be saved.' % number)
            articles[number] = article

        return articles

    @staticmethod
    def __get_number_of_articles(query):
        return int(query('#results-blk .results-display b:eq(1)').text())

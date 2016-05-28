import math
import requests
import re
from requests import Timeout
from pyquery import PyQuery
from app.models import Journal, Issue, Article
from mongoengine import DoesNotExist
from pymongo.errors import ServerSelectionTimeoutError
from app import logger
from app.ieee.citation import CitationLoader


class IEEECrawler:
    def __init__(self):
        pass

    @staticmethod
    def get_article(article_number):
        return ArticleCrawler(article_number)

    @staticmethod
    def get_journal(journal_number):
        return JournalCrawler(journal_number)

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


class JournalCrawler:
    def __init__(self, journal):
        if isinstance(journal, Journal):
            self.__journal = journal
        else:
            self.__journal = IEEECrawler.get_journal_object(str(journal))

    def __eq__(self, other):
        return isinstance(other, JournalCrawler) \
                and self.__journal == other.__journal

    @property
    def entry_number(self):
        return self.__journal.entry_number

    @property
    def name(self):
        return self.__journal.name

    def get_current_issue(self):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        payload = {
            'punumber': self.__journal.entry_number
        }
        r = requests.get(url, params=payload)

        query = PyQuery(r.text)
        text = query('#jrnl-issue-hdr h2').text().strip()
        current_year = int(text[-4:])
        issue_number = int(text[6])

        try:
            current_issue = Issue.objects.get(
                journal_reference=self.__journal,
                status=Issue.CURRENT_ISSUE
            )
            if current_issue.year == current_year \
                    and current_issue.number == issue_number:
                logger.info('Current issue has not been updated')
                return IssueCrawler(current_issue)
            else:
                logger.info('Current issue need to be updated')
                query_text = '#pi-%d li:eq(%d) a' % \
                             (current_issue.year, current_issue.number - 1)
                url = query(query_text).attr('href')
                current_issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)
                current_issue.status = Issue.PAST_ISSUE
                current_issue.save()
        except DoesNotExist:
            logger.info('Current issue does not exist in database')

        # does not exist or updated
        current_issue = Issue()
        current_issue.entry_number = 'current_' + self.__journal.entry_number
        current_issue.year = current_year
        current_issue.number = issue_number
        current_issue.journal_reference = self.__journal
        current_issue.status = Issue.CURRENT_ISSUE
        current_issue.save()
        logger.info('Current issue updated')
        return IssueCrawler(current_issue)

    def get_early_access(self):
        try:
            issue = Issue.objects.get(
                journal_reference=self.__journal,
                status=Issue.EARLY_ACCESS
            )
            return IssueCrawler(issue)
        except DoesNotExist:
            issue = Issue()

            url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
            payload = {
                'punumber': self.__journal.entry_number
            }
            r = requests.get(url, params=payload)
            query = PyQuery(r.text)
            url = query('#nav-article li:eq(2) a').attr('href')

            issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)
            issue.year = 0
            issue.number = 0
            issue.status = Issue.EARLY_ACCESS
            issue.is_current = False
            issue.journal_reference = self.__journal
            issue.save()

            return IssueCrawler(issue)

    def get_past_issue(self, year, number):
        try:
            issue = Issue.objects.get(
                journal_reference=self.__journal,
                year=year,
                number=number
            )
            return IssueCrawler(issue)
        except DoesNotExist:
            issue = Issue()
            issue.year = year
            issue.number = number
            issue.journal_reference = self.__journal
            issue.status = Issue.PAST_ISSUE

            url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
            payload = {
                'punumber': self.__journal.entry_number
            }
            r = requests.get(url, params=payload)
            query = PyQuery(r.text)

            query_text = '#pi-%d li:eq(%d) a' % \
                         (issue.year, issue.number - 1)
            url = query(query_text).attr('href')
            issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)

            issue.save()

            return IssueCrawler(issue)


class IssueCrawler:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, issue):
        if isinstance(issue, Issue):
            self.__issue = issue
        else:
            self.__issue = Issue.objects.get(entry_number=issue)
        self.__journal = issue.journal_reference

    def __eq__(self, other):
        return isinstance(other, IssueCrawler) \
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


class ArticleCrawler:
    def __init__(self, article):
        if isinstance(article, Article):
            self.__article = article
        else:
            self.__article = Article.objects.get(entry_number=str(article))

    def __eq__(self, other):
        return isinstance(other, ArticleCrawler) \
                   and self.__article == other.__article

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

    def bibtex(self):
        return str(self.__article)

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
            'status': self.status
        }

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


class JournalCrawler:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, journal_number):
        self.__journal_number = str(journal_number)
        self.__current_issue_file = \
            'out/' + self.__journal_number + '_current_issue.txt'
        self.__early_access_file = \
            'out/' + self.__journal_number + '_early_access.txt'
        self.__new_article_file = \
            'out/' + self.__journal_number + '_new_articles.txt'

        self.__journal = self.get_journal_object(journal_number)

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

    def get_current_issue(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        numbers = self.get_article_numbers(url)
        return self.get_articles(
            numbers,
            self.__current_issue_file if to_file else None
        )

    def get_early_access(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
        issue_number = self.get_early_access_number()
        numbers = self.get_article_numbers(url, issue_number=issue_number)
        return self.get_articles(
            numbers,
            self.__early_access_file if to_file else None
        )

    def get_new_articles(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
        numbers = self.get_article_numbers(url, skip_exists=True)
        return self.get_articles(
            numbers,
            self.__new_article_file if to_file else None
        )

    def update_current_issue_information(self):
        '''
        check whether the current issue is updated.
        if updated, update the number of the last issue before current issue.
        :return: [Year, Issue, Whether Updated]
        '''
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        payload = {
            'punumber': self.__journal_number
        }
        r = requests.get(url, params=payload)

        query = PyQuery(r.text)
        text = query('#jrnl-issue-hdr h2').text().strip()

        logger.debug(text)
        logger.debug(text[-4:])
        logger.debug(text[6])

        current_year = int(text[-4:])
        issue_number = int(text[6])

        try:
            current_issue = Issue.objects.get(
                journal_reference=self.__journal,
                is_current=True
            )
            if current_issue.year == current_year \
                    and current_issue.issue_number == issue_number:
                logger.info('Current issue has not been updated')
                return current_year, issue_number, False
            else:
                logger.info('Current issue need to be updated')
                query_text = '#pi-%d li:eq(%d) a' % \
                             (current_issue.year, current_issue.issue_number - 1)
                logger.debug('Finding url of the past issues via jquery: ' + query_text)
                url = query(query_text).attr('href')
                current_issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)
                logger.debug('entry_number:' + current_issue.entry_number)
                current_issue.is_current = False
                current_issue.save()
        except DoesNotExist:
            logger.info('Current issue does not exist in database')
            pass

        # does not exist or updated
        current_issue = Issue()
        current_issue.year = current_year
        current_issue.issue_number = issue_number
        current_issue.journal_reference = self.__journal
        current_issue.save()
        logger.info('Current issue updated')
        return current_year, issue_number, True

    def get_early_access_number(self):
        url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
        payload = {
            'punumber': self.__journal_number
        }
        r = requests.get(url, params=payload)

        query = PyQuery(r.text)
        issue_url = query('#nav-article li:eq(2) a').attr('href')
        return issue_url.split('=')[1]

    def get_article_numbers(self, url, issue_number=None, skip_exists=False):
        journal_number = self.__journal_number

        logger.info('Obtaining article numbers')

        payload = {
            'punumber': journal_number
        }

        if issue_number:
            payload['isnumber'] = issue_number

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
        number_of_articles = self.__get_number_of_article(query)

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
            if skip_exists:
                for number in tmp_numbers:
                    try:
                        Article.objects.get(article_number=number)
                    except DoesNotExist:
                        numbers.append(number)
            else:
                numbers.extend(tmp_numbers)

        logger.info('Article numbers obtained: %d articles' % number_of_articles)

        return numbers

    @staticmethod
    def get_articles(numbers, filename=None):
        if filename:
            with open(filename, 'w') as fid:
                fid.write('')

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

            try:
                article.save()
                logger.info('Article [%s] saved.' % number)
            except ServerSelectionTimeoutError:
                logger.info('Cannot connect to database, Article [%s] will not be saved.' % number)
            articles[number] = article

            if filename:
                with open(filename, 'a') as fid:
                    fid.write('Entry Number: %s\n' % number)
                    fid.write('Title: %s\n' % article.title)
                    fid.write('Author %s\n' % article.author)
                    fid.write('Abstract: %s\n' % article.abstract)
                    fid.write('Keyword: %s\n' % article.keyword)
                    fid.write('\n')

        return articles

    @staticmethod
    def __get_number_of_article(query):
        return int(query('#results-blk .results-display b:eq(1)').text())

import math
import requests
from requests import Timeout
from bs4 import BeautifulSoup
from app.models import Article
from mongoengine import DoesNotExist
from app import logger


class JournalCrawler:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, journal_number):
        self.__journal_number = str(journal_number)
        self.__current_issue_file =\
            'out/' + self.__journal_number + '_current_issue.txt'
        self.__early_access_file = \
            'out/' + self.__journal_number + '_early_access.txt'
        self.__new_article_file = \
            'out/' + self.__journal_number + '_new_articles.txt'

    def get_current_issue(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        numbers = self.__get_article_numbers(url)
        return self.__get_articles(
            numbers,
            self.__current_issue_file if to_file else None
        )

    def get_early_access(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
        numbers = self.__get_article_numbers(url)
        return self.__get_articles(
            numbers,
            self.__early_access_file if to_file else None
        )

    def get_new_articles(self, to_file=False):
        url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
        numbers = self.__get_article_numbers(url, skip_exists=True)
        return self.__get_articles(
            numbers,
            self.__new_article_file if to_file else None
        )

    def __get_article_numbers(self, url, skip_exists=False):
        logger.info('Obtaining article numbers')

        payload = {
            'punumber': self.__journal_number
        }

        r = None
        num_try = 1
        while True:
            try:
                logger.info('Page 1: Trying No. %d' % num_try)
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

        soup = BeautifulSoup(r.text, 'html.parser')

        number_of_articles = self.__get_number_of_article(soup)

        numbers = []

        for i in range(0, math.ceil(number_of_articles / self.INIT_ARTICLE_PER_PAGE)):

            if i > 0:
                payload['pageNumber'] = i + 1
                r = None
                num_try = 1
                while True:
                    try:
                        logger.info('Page %d: Trying No. %d' % (i + 1, num_try))
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
                soup = BeautifulSoup(r.text, 'html.parser')

            results = soup.find(id='results-blk').find(name='ul', class_='results')
            elems = results.find_all(name='li')
            tmp_numbers = [elem['aria-describedby'].split(' ')[0].split('-')[3]
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
    def __get_articles(numbers, filename):
        if filename:
            with open(filename, 'w') as fid:
                fid.write('')

        url = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp'
        articles = {}

        for number in numbers:
            logger.info('Crawling the information of article [%s]' % number)

            r = None
            num_try = 1
            while True:
                try:
                    logger.info('Trying No. %d' % num_try)
                    r = requests.get(url=url, params={
                        'arnumber': number
                    })
                    break
                except Timeout:
                    num_try += 1
                    if num_try > 10:
                        logger.info('Timeout')
                        break
            del num_try
            if not r:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')

            name_tag = soup.find(class_='title').find(name='h1')
            name = name_tag.string.strip()

            abstract_tag = soup.find(class_='article').find(name='p')
            abstract = str(abstract_tag)[3:-4]

            if not abstract:
                abstract = ''

            try:
                article = Article.objects.get(article_number=number)
                logger.info('Article [%s] already exists, it will be updated.' % number)
            except DoesNotExist:
                article = Article()
                article.article_number = number
                logger.info('Article [%s] saved.' % number)
            article.article_name = name
            article.abstract = abstract

            article.save()
            articles[number] = article

            if filename:
                with open(filename, 'a') as fid:
                    fid.write('Article Number: %s\n' % number)
                    fid.write('Article Name: %s\n' % article.article_name)
                    fid.write('Abstract: %s\n' % article.abstract)
                    fid.write('\n')

        return articles

    @staticmethod
    def __get_number_of_article(soup):
        results = soup.find(id='results-blk') \
            .find(class_='results-display') \
            .find_all(name='b')
        return int(results[1].string)
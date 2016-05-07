import math
import requests
from bs4 import BeautifulSoup


class JournalCrawler:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, journal_id):
        self.__journal_id = str(journal_id)

    def get_current_issue_abstracts(self):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        [numbers, names] = self.__get_articles(url)
        return names, self.__get_abstracts(numbers)

    def __get_articles(self, url):
        payload = {
            'punumber': self.__journal_id
        }
        r = requests.get(url=url, params=payload)

        soup = BeautifulSoup(r.text, 'html.parser')

        article_number = self.__get_article_number(soup)

        numbers = []
        names = {}

        for i in range(0, math.ceil(article_number / self.INIT_ARTICLE_PER_PAGE)):
            if i > 0:
                payload['pageNumber'] = i + 1
                r = requests.get(url=url, params=payload)
                soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find(id='results-blk').find(name='ul', class_='results')
            elems = results.find_all(name='li')
            tmp_numbers = [elem['aria-describedby'].split(' ')[0].split('-')[3]
                           for elem in elems]
            for number in tmp_numbers:
                span_to_find = results.find(id='art-abs-title-' + number)
                names[number] = span_to_find.string if span_to_find else ''
            numbers.extend(tmp_numbers)

        return numbers, names

    @staticmethod
    def __get_abstracts(numbers):
        url = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp'
        abstracts = {}
        for number in numbers:
            abstracts[number] = None
            r = requests.get(url=url, params={
                'arnumber': number
            })
            soup = BeautifulSoup(r.text, 'html.parser')
            abstract_tag = soup.find(class_='article').find(name='p')
            abstracts[number] = str(abstract_tag)[3:-4]

            if not abstracts[number]:
                abstracts[number] = ''
        return abstracts

    @staticmethod
    def __get_article_number(soup):
        results = soup.find(id='results-blk') \
            .find(class_='results-display') \
            .find_all(name='b')
        return int(results[1].string)

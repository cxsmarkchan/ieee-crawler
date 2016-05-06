import math
import requests
from bs4 import BeautifulSoup


class JournalCrawler:
    INIT_ARTICLE_PER_PAGE = 25

    def __init__(self, journal_id):
        self.__journal_id = str(journal_id)

    def get_current_issue_numbers(self):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        payload = {
            'punumber': self.__journal_id
        }
        r = requests.get(url=url, params=payload)

        soup = BeautifulSoup(r.text, 'html.parser')

        article_number = self.__get_article_number(soup)

        numbers = []

        for i in range(0, math.ceil(article_number / self.INIT_ARTICLE_PER_PAGE)):
            if i > 0:
                payload['pageNumber'] = i + 1
                r = requests.get(url=url, params=payload)
                soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find(id='results-blk').find(name='ul', class_='results')
            elems = results.find_all(name='li')
            numbers.extend(
                [elem['aria-describedby'].split(' ')[0].split('-')[3]
                 for elem in elems]
            )

        return numbers

    @staticmethod
    def __get_article_number(soup):
        results = soup.find(id='results-blk') \
            .find(class_='results-display') \
            .find_all(name='b')
        return int(results[1].string)

import requests


class CitationLoader:
    def __init__(self, article_numbers):
        self.__article_numbers = article_numbers

    @property
    def article_numbers(self):
        return self.__article_numbers

    @article_numbers.setter
    def article_numbers(self, value):
        self.__article_numbers = value

    def get_citations_html(self):
        url_for_cookie = 'http://ieeexplore.ieee.org'
        r_begin = requests.get(url_for_cookie)
        cookies = ';'.join([(cookie.name + '=' + cookie.value) for cookie in r_begin.cookies])

        url = 'http://ieeexplore.ieee.org/xpl/downloadCitations'
        headers = {
            'Cookie': cookies
        }
        data = {
            'recordIds': ','.join([str(number) for number in self.article_numbers]),
            'citations-format': 'citation-abstract',
            'download-format': 'download-bibtex',
        }

        r = requests.post(url=url, headers=headers, data=data)
        return r.text

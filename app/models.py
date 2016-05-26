from mongoengine import Document, IntField, StringField
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


class Article(Document):
    UNVISITED = 0
    VISITED = 1
    NEED_FURTHER = 2
    IMPORTANT = 3

    entry_number = IntField(required=True, primary_key=True)
    title = StringField(required=True)
    author = StringField()
    journal = StringField()
    year = StringField()
    volume = StringField()
    number = StringField()
    pages = StringField()
    abstract = StringField()
    keyword = StringField()
    doi = StringField()
    issn = StringField()
    status = IntField(required=True, default=UNVISITED)

    def __str__(self):
        bib = BibDatabase()
        bib.entries = [{
            'ENTRYTYPE': 'article',
            'ID': self.entry_number,
            'author': self.author,
            'journal': self.journal,
            'title': self.title,
            'year': self.year,
            'volume': self.volume,
            'number': self.number,
            'pages': self.pages,
            'abstract': self.abstract,
            'keyword': self.keyword,
            'doi': self.doi,
            'issn': self.issn
        }]
        return bibtexparser.dumps(bib)


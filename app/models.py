from mongoengine import Document, IntField, StringField, BooleanField, ReferenceField
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


class Journal(Document):
    entry_number = StringField(required=True, primary_key=True)
    name = StringField(required=True)

    def __str__(self):
        return str(self.name)


class Issue(Document):
    EARLY_ACCESS = 0
    CURRENT_ISSUE = 1
    PAST_ISSUE = 2

    entry_number = StringField(default='0')
    year = IntField(required=True)
    number = IntField(required=True)
    journal_reference = ReferenceField(Journal)
    status = IntField(required=True)

    def __str__(self):
        return 'Issue ' + str(self.issue_number) + ' / ' + str(self.year)


class Article(Document):
    UNVISITED = 0
    VISITED = 1
    NEED_FURTHER = 2
    IMPORTANT = 3

    entry_number = StringField(required=True, primary_key=True)
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
    issue_reference = ReferenceField(Issue)
    note = StringField(default='')

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

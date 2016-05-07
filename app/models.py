from mongoengine import Document, IntField, StringField


class Article(Document):
    article_number = IntField(required=True, primary_key=True)
    article_name = StringField(required=True)
    abstract = StringField()

    def __str__(self):
        return self.article_name


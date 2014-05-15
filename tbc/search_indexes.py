import datetime
from haystack import indexes
from models import Book, Chapters


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ChaptersIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(   document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Chapters

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        

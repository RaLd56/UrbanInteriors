from haystack import indexes
from .models import Good

class GoodIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    category = indexes.CharField(model_attr='category')
    description = indexes.CharField(model_attr='description')
    color = indexes.CharField(model_attr='color')
    style = indexes.CharField(model_attr='style')
    materials = indexes.CharField(model_attr='materials')


    def get_model(self):
        return Good

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

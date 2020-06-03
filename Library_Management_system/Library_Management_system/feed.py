from django.contrib.syndication.views import Feed
from django.urls import reverse
from management.models import Book

class LatestEnteriesFeed(Feed):
    title = 'E-Library'
    link = '/feed/'
    description = 'Following are latest book available.'

    def items(self):
        return Book.objects.order_by('-id')[:2]

    def item_title(self, item):
        return item.title

    def item_summary(self, item):
        return item.summary

    def item_link(self, item):
        return item.get_absolute_url()

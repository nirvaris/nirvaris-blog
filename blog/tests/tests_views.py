from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ..models import Post, Tag


class PageViewTestCase(TestCase):

    def setUp(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def _create_post_(post_content):
        ...
        
    def _create_tag_cook(slef):
        tag = Tag(name='cook')
        tag.save()
        return tag
    
    def _create_tag_vegan(slef):
        tag = Tag(name='vegan')
        tag.save()
        return tag
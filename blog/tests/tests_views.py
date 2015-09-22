from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ..models import Post, Tag


class PageViewTestCase(TestCase):

    def setUp(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.author = self._create_author()
        self.tag_cook = self._create_tag_cook()
        self.tag_vegan = self._create_tag_vegan()

    def tearDown(self):
        ...                  
        
    def _create_post_(post_content):
        post = Post(author=self.author, relative_url='nice_post',title='this is a nice post',content='<p>This is the post content</p>')
        
    def _create_tag_cook(slef):
        tag = Tag(name='cook')
        tag.save()
        return tag
    
    def _create_tag_vegan(slef):
        tag = Tag(name='vegan')
        tag.save()
        return tag
        
    def _create_author(self):
        
        user = User(first_name='Jack', last_name='Daniels',email='jack@daniels.com',username='jack')
        user.save()
        return user
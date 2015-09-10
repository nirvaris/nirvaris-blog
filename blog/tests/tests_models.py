from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Post

class BlogModelTestCase(TestCase):

    def setUp(self):
        self.author = self._create_author()

    def tearDown(self):
        ...
    
    def test_create_post(self):
        post = Post(author=self.author)
        post.save()

    
    def _create_author(self):
        
        user = User(first_name='Jack', last_name='Daniels',email='jack@daniels.com',username='jack')
        user.save()
        return user
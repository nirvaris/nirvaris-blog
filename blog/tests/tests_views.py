import pdb
import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ..models import Post, Tag, MetaTag, Comment


class PostViewTestCase(TestCase):

    def setUp(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.author = self._create_author()
        self.tag_cook = self._create_tag_cook()
        self.tag_vegan = self._create_tag_vegan()
        self.post_cook = self._create_post_cook()
        self.excited_comment_user = self._create_comment_user()

    def tearDown(self):
        ...                  
    
    def test_get_comment_with_author(self):
        
        comment = Comment(author=self.excited_comment_user, post=self.post_cook, content='A comment from an Excited user')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_post_cook')       
        
        self.assertIn(comment.content, str(response.content))
        self.assertIn(self.excited_comment_user.get_full_name(), str(response.content))         
            
    def test_get_comment_no_author(self):
        
        comment = Comment(post=self.post_cook, content='some very nice comment comment')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_post_cook')       
        
        self.assertIn(comment.content, str(response.content)) 
    
    def test_get_post_view(self):

        c = self.c

        response = c.get('/blog/nice_post_cook')
        
        self.assertEquals(response.status_code,200,'blog post')
        
        self.assertTrue(isinstance(response.context['post'], Post))
        
        self.assertTrue(any(self.post_cook.template in t.name for t in response.templates))
        
        self.assertIn(self.post_cook.content, str(response.content))

    def test_get_post_meta_tag(self):
    
        c = self.c

        response = c.get('/blog/nice_post_cook')
        
        content = str(response.content)        
        #pdb.set_trace()
        self.assertTrue(re.search(re.compile('<meta.+?name="keywords"'), content),
        'Meta tag name not found')

        self.assertTrue(re.search(re.compile('<meta.+?name="description"'), content),
        'Meta tag description not found')

        self.assertTrue(re.search(re.compile('<meta.+?property="twitter:card"'), content),
        'Meta tag twitter:card not found')
    
    def _create_post_cook(self):
        
        post = Post(author=self.author, relative_url='nice_post_cook',title='this is a nice post cook',content='<p>This is the post content</p>')
        post.save()
        
        meta_tag = MetaTag(post=post, name='keywords',content='some key words')
        meta_tag.save()
        
        meta_tag = MetaTag(post=post, name='description',content='some description')
        meta_tag.save()        
        
        meta_tag = MetaTag(post=post, property='twitter:card',content='sumary')
        meta_tag.save()
        
        return post

        
    def _create_tag_cook(slef):
        tag = Tag(name='cook')
        tag.save()
        return tag
    
    def _create_tag_vegan(slef):
        tag = Tag(name='vegan')
        tag.save()
        return tag
 
    def _create_comment_user(self):
     
        user = User(first_name='Exited', last_name='Comment User',email='excited@comment.user.com',username='excited')
        user.save()
        return user
        
    def _create_author(self):
        
        user = User(first_name='Jack', last_name='Daniels',email='jack@daniels.com',username='jack')
        user.save()
        return user
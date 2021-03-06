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

    def test_post_new_comment_existing_author(self):
        
        total_comments = Comment.objects.all().count()
        total_users = User.objects.all().count()
        c = self.c
        
        post_content = 'If you know him as long as I know, you know his name is John'
        
        response = c.post('/blog/nice_post_cook', {
            'name':'John Daniels',
            'email': 'excited@comment.user.com',
            'post_id': self.post_cook.id,
            'content': post_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        self.assertEquals(total_users,User.objects.all().count())
  
    def test_post_new_comment_new_author(self):
        
        total_comments = Comment.objects.all().count()
        total_users = User.objects.all().count()
        c = self.c
        
        post_content = 'If you know him as long as I do, you would know his name is John'
        
        response = c.post('/blog/nice_post_cook', {
            'name':'John Daniels',
            'email': 'john@daniels.com',
            'post_id': self.post_cook.id,
            'content': post_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        self.assertEquals(total_users+1,User.objects.all().count())
        
        new_user = User.objects.latest('id')
        new_comment = Comment.objects.latest('id')

        self.assertEqual(new_user,new_comment.author)

    def test_post_new_comment_with_name_no_email(self):

        c = self.c
        
        total_comments = Comment.objects.all().count()
        
        post_content = 'This is a comment from Jack Daniels already in the DB'
        
        response = c.post('/blog/nice_post_cook', {
            'name': 'No Email',
            'post_id': self.post_cook.id,
            'content': post_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments,Comment.objects.all().count())
           
    def test_post_new_comment_with_email_no_name(self):

        c = self.c
        
        total_comments = Comment.objects.all().count()
        
        post_content = 'This is a comment from Jack Daniels already in the DB'
        
        response = c.post('/blog/nice_post_cook', {
            'email': 'excited@comment.user.com',
            'post_id': self.post_cook.id,
            'content': post_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments,Comment.objects.all().count())
        
    def test_post_new_comment_no_author(self):
        
        total_comments = Comment.objects.all().count()
        
        c = self.c
        
        post_content = 'This is a comment posted via comment form'
        
        response = c.post('/blog/nice_post_cook', {
            'post_id':self.post_cook.id,
            'content': post_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        response = c.get('/blog/nice_post_cook')       
        
        self.assertNotIn(post_content, str(response.content))

    def test_get_comment_not_approved(self):
        
        comment = Comment(author=self.excited_comment_user,is_approved=False, post=self.post_cook, content='A comment from an Excited user')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_post_cook')       
        
        self.assertNotIn(comment.content, str(response.content))

        
    def test_get_comment_with_author(self):
        
        comment = Comment(author=self.excited_comment_user,is_approved=True, post=self.post_cook, content='A comment from an Excited user')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_post_cook')       
        
        self.assertIn(comment.content, str(response.content))
        self.assertIn(self.excited_comment_user.get_full_name(), str(response.content))         
            
    def test_get_comment_no_author(self):
        
        comment = Comment(post=self.post_cook,is_approved=True, content='some very nice comment comment')
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
        
        content = str(response.content)
        
        self.assertIn(self.post_cook.content, content)
        #pdb.set_trace()
        
        self.assertTrue(re.search(re.compile('<title>.*' + self.post_cook.title + '.*</title>'), content),
        'page title does not match')

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
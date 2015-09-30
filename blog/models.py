from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')    
    relative_url = models.CharField(max_length=100, unique=True, null=False)
    title = models.CharField(max_length=70, null=False)
    template = models.CharField(max_length=50, null=False, default='post-default.html')
    content = models.TextField(null=False)
    access_count = models.BigIntegerField(default=0,null=False)
    tags = models.ManyToManyField('Tag', related_name='tags')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title + ' (url: /' + self.relative_url + ')' 
        
class MetaTag(models.Model):
    name = models.CharField(max_length=70)
    property = models.CharField(max_length=70, null=True, blank=True)
    content  = models.CharField(max_length=70, null=True, blank=True)
    post = models.ForeignKey('Post', related_name='meta_tags')

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, related_name='post_comments') 
    post = models.ForeignKey(Post, related_name='post_comments') 
    content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)    
    def __str__(self):
        if self.author:
            return self.author.get_full_name()
        return 'Anonymous'

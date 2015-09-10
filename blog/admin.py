from django.contrib import admin

from .models import Post, MetaTag, Tag, Comment

admin.site.register(Post)
admin.site.register(MetaTag)
admin.site.register(Tag)
admin.site.register(Comment)
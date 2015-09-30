from django.contrib import admin

from .models import Post, MetaTag, Tag, Comment






class PostAdmin(admin.ModelAdmin):
    list_filter = ('author','title','relative_url','access_count',)
    list_display = ('author','title','relative_url','access_count',)
    search_fields = ['title','relative_url','content']

admin.site.register(Post, PostAdmin)

admin.site.register(MetaTag)
admin.site.register(Tag)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('post','author','content','is_approved','created')
    list_display = ('post','author','content','is_approved')
    list_editable = ('is_approved',)
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)

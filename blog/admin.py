from django.contrib import admin

from .models import Post, MetaTag, Tag, Comment

admin.site.register(Post)
admin.site.register(MetaTag)
admin.site.register(Tag)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('post','author','content','is_approved','created')
    list_display = ('post','author','content','is_approved')
    list_editable = ('is_approved',)
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)
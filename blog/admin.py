from django.contrib import admin

from .models import Post, MetaTag, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_filter = ('author','title','relative_url','access_count',)
    list_display = ('author','title','relative_url','access_count',)
    search_fields = ['title','relative_url','content']

admin.site.register(Post, PostAdmin)


class MetaTagAdmin(admin.ModelAdmin):
    list_filter = ('post','name','property','content')
    list_display = ('post','name','property','content')
    search_fields = ['name','property','content']
    
admin.site.register(MetaTag, MetaTagAdmin)


class TagAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ['name',]
    
admin.site.register(Tag,TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('post','author','content','is_approved','created')
    list_display = ('post','author','content','is_approved')
    list_editable = ('is_approved',)
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)

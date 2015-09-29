import pdb


from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.base import View
# Create your views here.

from .forms import CommentForm
from .models import Post

class PostView(View):
    
    def get(self, request, tags):
        
        tag_list = tags.split('/')
        #pdb.set_trace()
        if Post.objects.filter(relative_url=tag_list[-1]).exists():
        
            post = Post.objects.get(relative_url=tag_list[-1])
            post.access_count += 1
            post.save()
            form_initial = {'post_id': post.id}
            
            #pdb.set_trace()
            
            if request.user.is_authenticated():
                form_initial['email'] = request.user.email
                form_initial['name'] = request.user.get_full_name()
            
            form = CommentForm(initial=form_initial)
            form.anti_spam()
            
            request_context = RequestContext(request,{'post':post,'form':form})

            return render_to_response(post.template, request_context)
        
        #pdb.set_trace()

        if tag_list[0]!='':
            posts = Post.objects.filter(tags__name__iexact=tag_list.pop(0))
            for tag in tag_list:
                posts = posts.filter(tags__name__iexact=tag)
        else:
            posts = Post.objects.all()
            
        request_context = RequestContext(request,{'posts':posts})
        
        return render_to_response('posts-tags.html', request_context)

    def post(self, request, tags):
        
        form = CommentForm(request.POST)
        
        form_valid = form.is_valid()
        cleaned_data = form.clean()
            
        post = Post.objects.get(id=cleaned_data['post_id'])
        
        if form_valid:
            form.save()
            form = CommentForm(initial={'post_id': post.id})
        
        form.anti_spam()
        
        request_context = RequestContext(request,{'post':post,'form':form})

        return render_to_response(post.template, request_context)
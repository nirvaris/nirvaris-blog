import pdb
import uuid

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import Comment



class CommentForm(forms.ModelForm):

    name = forms.CharField(required=False, label=_('Name'), max_length=200)
    email = forms.EmailField(required=False, label=_('Email'), max_length=200)
    post_id = forms.CharField(required=True, widget=forms.HiddenInput())

    anti_spam_token = forms.CharField(widget=forms.HiddenInput())
    anti_spam_hidden = forms.CharField(widget=forms.HiddenInput())
    anti_spam_no_hidden = forms.CharField(required=False,label='')

    class Meta:
        model = Comment
        fields =[
            'post_id' ,'name', 'email', 'content'
        ]

    def anti_spam(self):
        
        spam_token = uuid.uuid4()
        
        self.initial['anti_spam_token'] = str(spam_token)
        self.initial['anti_spam_no_hidden'] = str(spam_token) 
        self.initial['anti_spam_hidden'] = ''  
                
    def clean(self):
        
        cleaned_data = super(CommentForm, self).clean()
        #pdb.set_trace()
        #if cleaned_data['anti_spam_hidden'] != cleaned_data['anti_spam_token'] or 'anti_spam_no_hidden' in cleaned_data:
        #    self.add_error(None,_('Are you human?'))
        #    return cleaned_data            
        
        
        name = ''
        email = ''
        try:
            name = cleaned_data['name']
            email = cleaned_data['email']
        except:
            pass
        
        if name != '' or email != '':
            if name == '' or email == '':
                self.add_error('name',_('You have to inform both, email and name, otherwise, leave both blank.'))
                return cleaned_data
        
        self.author = None
        if email != '':
            if User.objects.filter(email=email).exists():
                self.author = User.objects.get(email=email)
            else:
                self.author = User(username=email, email=email)

            first_name = name.split(' ')[0].strip()
            last_name = name.replace(first_name, '').strip()

            self.author.first_name = first_name
            self.author.last_name = last_name

        self.instance.post_id = cleaned_data['post_id']
        
        return cleaned_data
    
    def save(self, commit=True):
        
        if commit:
            if self.author:
                self.author.save()
                self.instance.author = self.author
            self.instance.save()
        
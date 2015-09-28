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
    anti_spam_no_hidden = forms.CharField(label='')

    def __init__(self, *args, **kwargs):
        
        spam_token = uuid.uuid4()
        
        initial = kwargs.get('initial', {})
        initial['anti_spam_token'] = str(spam_token)
        initial['anti_spam_no_hidden'] = str(spam_token)   
             
        kwargs['initial'] = initial
        super(CommentForm, self).__init__(*args, **kwargs)

    
    class Meta:
        model = Comment
        fields =[
            'post_id' ,'name', 'email', 'content'
        ]

    

    def clean(self):
        
        cleaned_data = super(CommentForm, self).clean()
        
        if cleaned_data['anti_spam_hidden'] != cleaned_data['anti_spam_token'] or 'anti_spam_no_hidden' in cleaned_data:
            self.add_error(None,_('Are you human?'))
            return cleaned_data            
        
        
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
        
        if email != '':
            if User.objects.filter(email=email).exists():
                self.instance.author = User.objects.get(email=email)
            else:
                self.instance.author = User(username=email, email=email)

            first_name = name.split(' ')[0].strip()
            last_name = name.replace(first_name, '').strip()

            self.instance.author.first_name = first_name
            self.instance.author.last_name = last_name

        self.instance.post_id = cleaned_data['post_id']

        return cleaned_data
    
    def save(self, commit=True):
        
        if commit:
            if self.instance.author:
                self.instance.author.save()
            self.instance.save()
        
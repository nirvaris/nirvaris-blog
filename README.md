#Nirvaris Blog

A simple Django app to add blog post with comments and meta-tags to your website, using tags for listing.

You add posts and tags via django admin interface and they will be avaliable in your website.

you use it like:

```
<your-url>/blog/<relative_url> # return the blog post
<your-url>/blog/<tag>/<tag>... # return a list of posts whithin these tags.
```

It uses the follow dependecies from Nirvaris:

- [Nirvaris Default Theme](https://github.com/nirvaris/nirvaris-theme-default)
- [Nirvaris Profile](https://github.com/nirvaris/nirvaris-profile)

A requirements file is provided with some other dependencies from PyPi.

#Quick start

To install the Blog, use pip from git:

```
pip install git+https://github.com/nirvaris/nirvaris-blog
```

- Your INSTALLED_APPS setting should look like this::

```
    INSTALLED_APPS = (
        ...
        'blog',
        'n_profile',
        'themedefault',
    )
```

- You have to run migrate, as it uses the db to store the posts, oomments and meta-tags. 

- You can add specific templates for the post, or it will use the default one, based on the theme.
	
- You hvae to add the app url to your url file:

```
url(r'^blog/', include('blog.urls')),
```
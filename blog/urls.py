from django.conf.urls import include, url
from django.contrib import admin

from .views import PostView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('n_profile.urls')),
    url(r'^(?P<tags>.*)$', PostView.as_view()),

]

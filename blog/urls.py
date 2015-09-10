from django.conf.urls import url

from .views import PostView

urlpatterns = [
    url(r'^(?P<tags>.*)$', PostView.as_view()),

]
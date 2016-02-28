from django.conf.urls import patterns, url, include

from api import views

urlpatterns = [
    url(r'^$', views.StoryList.as_view(), name='home'),
    url(r'^story/(?P<story>[0-9]+)/comments$', views.StoryComments.as_view(), name='comments'),
    url(r'^duration/(?P<duration>[0-9]+)$', views.StoryFilter.as_view(), name='filtered'),
    url(r'^submit$', views.StorySubmit.as_view(), name='submit'),
]

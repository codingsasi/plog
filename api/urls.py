from django.conf.urls import patterns, url, include

from api import views

urlpatterns = [
    url(r'^$', views.StoryList.as_view(), name='api-home'),
    url(r'^story/(?P<story>[0-9]+)/comments$', views.StoryComments.as_view(), name='api-comments'),
    url(r'^duration/(?P<duration>[0-9]+)$', views.StoryFilter.as_view(), name='api-filter'),
    url(r'^submit$', views.StorySubmit.as_view(), name='api-submit'),
    #url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^login/$', views.Login.as_view(), name='api-login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

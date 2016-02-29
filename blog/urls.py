from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^story/(?P<id>[0-9]+)/comments$', views.story, name='story'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup$', views.signup_view, name='signup'),
    url(r'^vote$', views.vote, name='vote')
]

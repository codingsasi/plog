from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from blog.models import Story, Vote, Comment

def home(request):
    stories = get_all_stories()
    template = loader.get_template('blog/home.html')
    return HttpResponse(template.render({'stories': stories}, request))

def get_all_stories():
    strs = Story.objects.all()
    stories = []
    for stry in strs:
        story = Story.objects.get(pk=stry.id)
        stories.append(story)
    return stories

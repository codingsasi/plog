from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone
from blog.models import Story, Vote, Comment
from api.views import StoryList
from datetime import datetime
import lxml.html

def home(request):
    stories = Story.objects.order_by('-upvotes')[0:5]
    for story in stories:
        upvotes = Vote.get_upvotes(story_id=story.id)
        downvotes = Vote.get_downvotes(story_id=story.id)
        Story.update_votes(story_id=story.id, upvotes=upvotes, downvotes=downvotes)
    template = loader.get_template('blog/home.html')
    return HttpResponse(template.render({'stories': stories}, request))

def submit(request):
    template = loader.get_template('blog/submit.html')
    pub_date = datetime.today().isoformat(' ')
    return HttpResponse(template.render({'pub_date': pub_date}, request))

def story(request, id):
    template = loader.get_template('blog/story.html')
    story = get_object_or_404(Story, id=id)
    try:
        story_html = lxml.html.parse(story.story_link)
        story_long_title = story_html.find(".//title").text
        story_teaser = story_html.find(".//p").text
    except:
        story_long_title = None
        story_teaser = None
    try:
        comments = Comment.objects.filter(story=id)
    except Comment.DoesNotExist:
        comments = None
    upvotes = Vote.get_upvotes(story.id)
    downvotes = Vote.get_downvotes(story.id)
    Story.update_votes(story_id=story.id, upvotes=upvotes, downvotes=downvotes)
    return HttpResponse(template.render({'story': story, 'comments': comments, 'comment_count': comments.count, 'story_long_title': story_long_title, 'story_teaser': story_teaser}, request))

def login_view(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

    return render_to_response('login.html',{'username': username}, context_instance=RequestContext(request))

def signup_view(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
    logout(request)
    user = User.objects.create_user('username', 'email', 'password')
    return render_to_response('login.html',{'username': username}, context_instance=RequestContext(request))

def vote(request):
    if request.POST:
        vote = request.POST.get('vote')
        user = request.POST.get('user')
        story = request.POST.get('story')

    try:
        vote_object = Vote.objects.get(story=story, user=user)
    except Vote.DoesNotExist:
        vote_object = None

    if vote == 'upvote':
        if vote_object == None:
            vote_object = Vote(vote=1, story_id=story, user_id=user)
            vote_object.save()
        elif vote_object.vote == 1:
            pass
        elif vote_object.vote == -1:
            vote_object.vote = 1
            vote_object.save()

    elif vote == 'downvote':
        if vote_object == None:
            vote_object = Vote(vote=-1, story_id=story, user_id=user)
            vote_object.save()
        elif vote_object.vote == -1:
            pass
        elif vote_object.vote == 1:
            vote_object.vote = -1
            vote_object.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

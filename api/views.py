from rest_framework import status
from django.shortcuts import render
from django.core.urlresolvers import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
import datetime
from django.utils import timezone
from blog.models import Story, Vote, Comment
from blog.views import *
from api.serializers import StorySerializer, CommentSerializer, VoteSerializer, LoginSerializer, UserSerializer
from api.permissions import IsAuthorOrReadOnly
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout

class Login(ListAPIView):

    serializer_class = LoginSerializer

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        credentials = LoginSerializer(data=request.data)

        if not credentials.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Okay, security check complete. Log the user in.
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

def signup(request):
    return HttpResponseRedirect(reverse('home'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

class StoryList(ListAPIView):
    """
    List popular stories.
    """
    queryset = Story.objects.filter(no_promote=False).order_by('-upvotes')
    serializer_class = StorySerializer
    paginate_by = 5

    #get top 5 voted posts
    def home(self, request):
        queryset = self.get_queryset()
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data)

class StorySubmit(ListCreateAPIView):
    """
    Submits a story.
    """
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def submit(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoryComments(ListCreateAPIView):
    """
    List all the comments of a story.
    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    def get_queryset(self):
        """
        This view should return a list of all the comments for
        the story mentioned in the url.
        """
        story = self.kwargs['story']
        return Comment.objects.filter(story=story)

    def comments(self, request):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

class StoryFilter(ListAPIView):
    """
    List Stories filtered by the time they were published.
    """
    serializer_class = StorySerializer
    def get_queryset(self):
        """
        This view takes duration in hours as argument, and it would show the
        stories from that time frame.
        """
        duration = self.kwargs['duration']
        timeframe = timezone.now() - datetime.timedelta(hours=int(duration))
        stories = Story.objects.filter(pub_date__range=[timeframe, timezone.now()]).order_by('-upvotes')
        return stories

    def filtered(self, request):
        queryset = self.get_queryset()
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
import datetime
from django.utils import timezone
from blog.models import Story, Vote, Comment
from api.serializers import StorySerializer, CommentSerializer, VoteSerializer
from api.permissions import IsUserOrReadOnly

class StoryList(ListAPIView):
    """
    List popular stories.
    """
    queryset = Story.objects.order_by('-upvotes')
    serializer_class = StorySerializer
    permission_classes = (IsUserOrReadOnly, )
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

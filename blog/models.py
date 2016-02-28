from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Story(models.Model):
    """
    The Object 'Story' that holds the link, tittle and other info.
    Upvotes and downvotes are updated as and when a user votes.
    The admin can decide whether or not a story should be displayed on the front
    page. IF 'no_promote' field  is checked, then it will not be displayed on the
    front page even if the story has max votes.
    """
    user = models.ForeignKey(User)
    story_title = models.CharField(max_length=255)
    story_link = models.URLField(max_length=500)
    pub_date = models.DateTimeField('date published')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    no_promote = models.BooleanField(default=False)

    def __str__(self):
        return self.story_title

    def get_upvotes(user):
        return 1

    def get_downvotes(user):
        return -1

class Vote(models.Model):

    vote = models.BooleanField()
    story = models.ForeignKey(Story)
    user = models.ForeignKey(User)

class Comment(models.Model):

    comment_title  = models.CharField(max_length=255)
    comment_body = models.TextField()
    story = models.ForeignKey(Story)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.comment_title

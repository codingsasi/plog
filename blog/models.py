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
    user = models.ForeignKey('auth.User', related_name='stories')
    story_title = models.CharField(max_length=255)
    story_link = models.URLField(max_length=500)
    pub_date = models.DateTimeField('date published')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    no_promote = models.BooleanField(default=False)

    def __str__(self):
        return self.story_title

    def update_votes(story_id, upvotes, downvotes):
        story = Story.objects.get(id=story_id)
        story.upvotes = upvotes
        story.downvotes = downvotes
        story.save()

class Vote(models.Model):
    """
    The object vote. Every user has one vote for every Story object.
    """
    vote = models.SmallIntegerField()
    story = models.ForeignKey(Story)
    user = models.ForeignKey('auth.User', related_name='votes')

    def get_upvotes(story_id):
        votes = Vote.objects.filter(story_id=story_id, vote=1)
        return votes.count()

    def get_downvotes(story_id):
        votes = Vote.objects.filter(story_id=story_id, vote=-1)
        return votes.count()

class Comment(models.Model):
    """
    The object comment. Every user can comment on any story.
    """
    comment_title  = models.CharField(max_length=255)
    comment_body = models.TextField()
    story = models.ForeignKey(Story)
    user = models.ForeignKey('auth.User', related_name='comments')

    def __str__(self):
        return self.comment_title

    def get_comment_count(story_id):
        comments = Comment.objects.filter(story_id=story_id)
        return comments.count()

from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):

    user = models.ForeignKey(User)
    story_title = models.CharField(max_length=255)
    story_link = models.URLField(max_length=500)
    pub_date = models.DateTimeField('date published')
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    promote_to_front_page = models.BooleanField()

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

    def __str__(self):
        return self.comment_title

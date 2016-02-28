from rest_framework import serializers
from django.contrib.auth.models import User

from blog.models import Story, Vote, Comment


class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ('user', 'story_title', 'story_link', 'pub_date', 'upvotes', 'downvotes', 'no_promote')

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('vote', 'story' , 'user')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_body', 'comment_title', 'story', 'user')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

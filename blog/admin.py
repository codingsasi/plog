from django.contrib import admin

from .models import Story, Vote, Comment

admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Vote)

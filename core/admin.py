from django.contrib import admin

from .models import Like, Post, Comment, Share

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Share)
admin.site.register(Post)

from rest_framework import serializers
from authentication.models import User
from core.models import Notification, Post, Like, Comment, Share
from django.urls import reverse


class UserMiniSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='name')

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'city', 'country', 'date_of_birth', 'image')


class NotificationsSerializer(serializers.ModelSerializer):
    by = UserMiniSerializer()
    url = serializers.SerializerMethodField('get_notification_url')

    def get_notification_url(self, obj):
        return reverse("core:notification", args=[obj.pk])

    class Meta:
        model = Notification
        fields = ('id', 'type', 'by', 'post_id', 'url')


class UserSerializer(serializers.ModelSerializer):
    notifications = NotificationsSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'city', 'country', 'date_of_birth', 'image',
                  'notifications', 'gender', 'friends', 'created_at')


class LikeSerializer(serializers.ModelSerializer):
    by = UserMiniSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'created_at', 'by')


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserMiniSerializer(read_only=True)
    likes = LikeSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'commenter', 'likes', 'message')


class ShareSerializer(serializers.ModelSerializer):
    shared_by = UserMiniSerializer(read_only=True)

    class Meta:
        model = Share
        fields = ('id', 'created_at', 'shared_by', 'message')


class PostSerializer(serializers.ModelSerializer):
    poster = UserMiniSerializer()
    likes = LikeSerializer()
    comments = CommentSerializer()
    shares = ShareSerializer()

    class Meta:
        model = Post
        fields = ('id', 'created_at', 'caption', 'post_image', 'public', 'poster', 'likes', 'comments', 'shares')

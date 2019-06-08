from rest_framework import serializers
from authentication.models import User
from core.models import Notification
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

from django.urls import path
from .views import (SendFriendRequest, NotificationsView, CreatePost, LikeApi, UnlikeApi, CommentApi, SharePostApi,
                    SearchAPI, EditProfileApi, ChangePasswordApi)

app_name = "api"

urlpatterns = [
    path('send-friend-request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('notifications/<uuid:user_id>', NotificationsView.as_view(), name="notifications"),
    path('create-post/', CreatePost.as_view(), name="create-post"),
    path('like-post/', LikeApi.as_view(), name='like-post'),
    path('unlike-post/', UnlikeApi.as_view(), name='unlike-post'),
    path('comment-post/', CommentApi.as_view(), name='comment-post'),
    path('share-post/', SharePostApi.as_view(), name='share-post'),
    path('search/', SearchAPI.as_view(), name='search'),
    path('edit-profile/<uuid:pk>', EditProfileApi.as_view(), name='edit-profile'),
    path('change-password/<uuid:pk>', ChangePasswordApi.as_view(), name='change-password'),
]

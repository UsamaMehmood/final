from django.urls import path, include

from .views import DashboardView, NotificationView, SearchResults, FriendsSuggestionView

app_name = 'core'

urlpatterns = [
    path('api/', include('core.api.urls', namespace='api')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('notification/<uuid:pk>', NotificationView.as_view(), name='notification'),
    path('search-results/', SearchResults.as_view(), name='search-results'),
    path('friends-suggestions/', FriendsSuggestionView.as_view(), name='friends-suggestions'),
]

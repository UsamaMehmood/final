from django.urls import path

from .views import LoginView, CompleteSignupView, LogoutView

app_name = "auth"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('complete-signup/<uuid:user_id>', CompleteSignupView.as_view(), name='complete_signup'),
]

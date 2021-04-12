from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import UserSignupView, UserLoginView

urlpatterns = [
    path("signup/", UserSignupView.as_view()),
    path("login/", UserLoginView.as_view()),
]
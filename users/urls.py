from django.urls import path

from users.views import *

urlpatterns = [
    path('/google', GoogleCallBackView.as_view()),
    path('/test', GoogleAccessTokenView.as_view()),
]   
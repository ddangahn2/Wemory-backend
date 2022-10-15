from django.urls import path

from users.views import *

urlpatterns = [
    path('/google', GoogleCallBackView.as_view()),
    path('/test', GoogleSignUpView.as_view()),
    path('/modify', ModifyView.as_view())
]   
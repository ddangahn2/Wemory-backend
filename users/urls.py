from django.urls import path

from users.views import *

urlpatterns = [
    path('/google', GoogleCallBackView.as_view()),
    path('/test', TestView.as_view()),
    path('/test2', WemoryView.as_view())
]   
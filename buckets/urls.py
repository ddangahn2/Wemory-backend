from django.urls import path

from buckets.views import *

urlpatterns = [
    path('', BucketListView.as_view()),
]   
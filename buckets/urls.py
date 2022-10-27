from django.urls import path

from buckets.views import *

urlpatterns = [
    path('/member', MemberBucketListView.as_view()),
    path('/nonmember', NonmemberBucketListView.as_view()),
]   
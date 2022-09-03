from django.urls import path

from .views import BucketListView, BucketDetailView

urlpatterns = [
    path('', BucketListView.as_view()),
    path('/<int:bucket_id>', BucketDetailView.as_view())
]

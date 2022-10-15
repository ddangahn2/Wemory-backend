from msilib.schema import Class
from django.shortcuts import render
from django.views import View

from buckets.models import * 
# Create your views here.

<<<<<<< HEAD
=======
class BucketView(View): # 데코레이터 달자
    def get(self, requset):
        title = requset.GET.get

        # 필터셋 , q객체 다써서 만들어보기 // 추가구현 가능하면 ES 사용

    def post(self, requset):
        new_bucket, is_created = Bucket.objects.get_or_create(bucket_id = requset['id']) # 버켓아이디
        
        new_bucket.title  = requset['title']
        new_bucket.public = requset['public']
        
        if is_created:
            new_bucket.user     = requset['user'] # 수정
            new_bucket.ordinal  = requset['ordinal'] # 수정

    def delete(self, request):
        delete_bucket = Bucket.objects.delete(bucket_id = request['bucket_id'])
>>>>>>> 4cd12193e17f963b96d20b2b57fb59f9d1a687ae

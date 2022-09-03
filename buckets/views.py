import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from buckets.models import *

class BucketListView(View): 
    #TODO : Decorator
    def get(self, request):
        title   = request.GET.get('title', None)
        ordinal = request.GET.get('ordinal', None)
        public  = request.GET.get('public', True)

        sorting = request.GET.get('order-by', 'latest')
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 12))
        
        sorting_dict = {
            'latest' : '-created_at'
        }
        
        # TODO : 필터셋 , q객체 다써서 만들어보기 // 추가구현 가능하면 ElasticSearch 사용
        q = Q()
        if title:
            q &= Q(bucket__title__in=title)
            
        filtered_buckets = Bucket.objects.filter(q)
        buckets          = filtered_buckets.order_by(sorting_dict[sorting])[offset:offset+limit]
        
        bucket_list = [{
            'id'     : bucket.id,
            'title'  : bucket.title,
            'user'   : bucket.user,
            'ordinal': bucket.ordinal,
            'public' : bucket.public
        } for bucket in buckets]
        
        return JsonResponse({'result' : bucket_list}, status=200)
    
class BucketDetailView(View):
    def get(self, request, bucket_id):
        try:
            bucket = Bucket.objects.get(id = bucket_id)
            papers = Paper.objects.get(bucket = bucket_id)

            result = {
                'id'           : bucket.id,
                'title'         : bucket.title,
                'ordinal'        : bucket.ordinal,
                'public'       : bucket.public,
                'papers' : [{
                    'paper_id' : paper.id,
                    'user'      : {
                        'name': paper.user.name,
                        'google_email'     : paper.user.email
                        },
                    'content'   : paper.content,
                    'created_at': paper.created_at
                }for paper in papers.all()]
            }
        
            return JsonResponse({'result' : result}, status=200)
        
        except Bucket.DoesNotExist:
            return JsonResponse({'message' : 'BUCKET_NOT_EXIST'}, status=404)
    
    # TODO : Paper 생성
    # @check_token
    # def post(self, request, bucket_id):
    #     try:
    #         data    = json.loads(request.body)
    #         bucket = Bucket.objects.get(id = bucket_id)
    #         user    = request.user

    #         Paper.objects.create(
    #             user    = user,
    #             bucket = bucket,
    #             content = data['content']
    #         )

    #         return JsonResponse({'message' : 'CREATED'}, status=201)
        
    #     except Bucket.DoesNotExist:
    #         return JsonResponse({'message' : 'BUCKET_NOT_EXIST'}, status=404)        
    
    # TODO : Paper 삭제
    # @check_token
    # def delete(self, request, bucket_id):
    #     paper_id = request.GET.get('paper-id', None)
    #     user      = request.user
    #     paper   = Paper.objects.filter(id = paper_id, bucket_id = bucket_id ,user = user)

    #     if not paper.exists():
    #         return JsonResponse({'message' : 'PAPER_NOT_EXIST'}, status = 404)
        
    #     paper.delete()
    #     return JsonResponse({'message' : 'SUCCESS'}, status = 204)    

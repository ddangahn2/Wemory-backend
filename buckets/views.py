import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from buckets.models import *
from users.models import *

from utilities.logindecorator import login_decorator

class MemberBucketListView(View): 
    @login_decorator
    def get(self, request):
        title   = request.GET.get('title', None)
        ordinal = request.GET.get('ordinal', None)
        writer  = request.GET.get('writer', None)

        sorting = request.GET.get('order-by', 'latest')
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 5))
        
        sorting_dict = {
            'latest': '-created_at',
            'old'   : 'created_at'
        }
        
        #TODO : 딕셔너리로 필터셋 구현
        q = Q()
        if title:
            q &= Q(title=title)
        if ordinal:
            q &= Q(ordinal=ordinal)
        if writer:
            q &= Q(user__name=writer)
                
        filtered_buckets = Bucket.objects.filter(q)
        buckets          = filtered_buckets.order_by(sorting_dict[sorting])[offset:offset+limit] 
        
        bucket_list = [{
            'id'     : bucket.id,
            'title'  : bucket.title,
            'user'   : bucket.user_id,
            'ordinal': bucket.ordinal_id,
            'public' : bucket.public
        } for bucket in buckets]
        
        return JsonResponse({'result' : bucket_list}, status=200)
    
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user

            ordinal_id = user.ordinal_id
            ordinal    = Ordinal.objects.get(id = ordinal_id)
            
            background_color_id = data['background_color']
            background_color    = Background_color.objects.get(id = background_color_id)
            
            Bucket.objects.create(
                title            = data['title'],
                user             = user,
                ordinal          = ordinal,
                public           = data['public'],
                background_color = background_color
            )

            return JsonResponse({'message' : 'CREATED'}, status=201)
        
        except Bucket.DoesNotExist:
            return JsonResponse({'message' : 'BUCKET_NOT_EXIST'}, status=404) 
        
class NonmemberBucketListView(View): 
    def get(self, request):
        title   = request.GET.get('title', None)
        ordinal = request.GET.get('ordinal', None)
        writer  = request.GET.get('writer', None)
        public  = request.GET.get('public', True)

        sorting = request.GET.get('order-by', 'latest')
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 5))
        
        sorting_dict = {
            'latest': '-created_at',
            'old'   : 'created_at'
        }
        
        q = Q()
        q &= Q(public=True)
        if title:
            q &= Q(title=title)
        if ordinal:
            q &= Q(ordinal=ordinal)
        if writer:
            q &= Q(user__name=writer)
                
        filtered_buckets = Bucket.objects.filter(q)
        buckets          = filtered_buckets.order_by(sorting_dict[sorting])[offset:offset+limit] 
        
        bucket_list = [{
            'id'     : bucket.id,
            'title'  : bucket.title,
            'user'   : bucket.user_id,
            'ordinal': bucket.ordinal_id,
            'public' : bucket.public
        } for bucket in buckets]
        
        return JsonResponse({'result' : bucket_list}, status=200)
        
# TODO : PaperView(BucketDetailView)
# class BucketDetailView(View):
#     def get(self, request, bucket_id):
#         try:
#             bucket = Bucket.objects.get(id = bucket_id)
#             papers = Paper.objects.get(bucket = bucket_id)

#             result = {
#                 'id'           : bucket.id,
#                 'title'         : bucket.title,
#                 'ordinal'        : bucket.ordinal,
#                 'public'       : bucket.public,
#                 'papers' : [{
#                     'paper_id' : paper.id,
#                     'user'      : {
#                         'name': paper.user.name,
#                         'google_email'     : paper.user.email
#                         },
#                     'content'   : paper.content,
#                     'created_at': paper.created_at
#                 }for paper in papers.all()]
#             }
        
#             return JsonResponse({'result' : result}, status=200)
        
#         except Bucket.DoesNotExist:
#             return JsonResponse({'message' : 'BUCKET_NOT_EXIST'}, status=404)
    
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

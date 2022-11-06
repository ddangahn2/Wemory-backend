import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from buckets.models import *
from users.models import *

from datetime import datetime

from utilities.logindecorator import login_decorator

class BucketListView(View): 
    # @login_decorator
    def get(self, request):
        
        title   = request.GET.get('title', None)
        ordinal = request.GET.get('ordinal', None)
        writer  = request.GET.get('writer', None)
        # public  = request.GET.get('public', True)

        sorting = request.GET.get('order-by', 'latest')
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 5))
        
        sorting_dict = {
            'latest': '-created_at',
            'old'   : 'created_at'
        }
        
        # TODO : 필터셋 , q객체 다써서 만들어보기 // 추가구현 가능하면 ElasticSearch 사용, 깃수별, search(타이틀, 생성자)
        q = Q()
        if title:
            q &= Q(title=title)
        if ordinal:
            q &= Q(ordinal=ordinal)
        if writer:
            q &= Q(user__name=writer)
        # if :
        #     if public == true:
        #     else:
        #         q &= Q(public=public)
                
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
        
class BucketPaperView(View):
    # 버킷 아이디 받으면 버킷안에 페이퍼 데이터 모두 주기
    @login_decorator
    def get(self, request):
        user   = request.user
        data   = json.loads(request.body)
        bucket = Bucket.objects.get(id = data['bucket_id'])

        if user.admin.title == 'guest' and paper.bucket.public==0:
            return JsonResponse({'message' : 'permission denied'})
        else:
            papers = bucket.paper_set.all()

            result = [{
                "paper_id"         : paper.id,
                "content"          : paper.content,
                "x_axis"           : paper.x_axis,
                "y_axis"           : paper.y_axis,
                "background_color" : paper.background_color.color_code,
                "font"             : paper.font.name,
                "font_color"       : paper.font_color.color_code,
                "font_size"        : paper.font_size.size
            } for paper in papers]

            return JsonResponse({'result' : result}, status = 200)

class PaperView(View):    
    # 페이퍼 생성
    @login_decorator
    def post(self, request):
        user   = request.user
        data   = request.POST
        images = request.FILES.getlist('image')

        paper = Paper.objects.create(
            bucket           = Bucket.objects.get(id = data['bucket_id']),
            user             = User.objects.get(id = user.id),
            content          = data['content'],
            x_axis           = data['x_axis'],
            y_axis           = data['y_axis'],
            background_color = data['background_color'],
            font             = data['font'],
            font_color       = data['font_color'],
            font_size        = data['font_size']
        )
        image_list = []

        for image in images:
            image_url = self.image_upload(image)
            image_list.append(Paper_image(paper = paper, image_url = image_url))

        Paper_image.objects.bulk_create(image_list)
    
    # 페이지 수정 (아직 bucket쪽 로직 수정해야함 + 프론트쪽 미구현)
    @login_decorator
    def patch(self, request):
        user  = request.user
        data  = request.POST
        paper = Paper.objects.get(id = data['id'])
        # 지우는 이미지
        del_images = request.FILES.getlist('del_image')
        # 추가시키는 이미지
        add_images = request.FILES.getlist('add_image')

        del_image_list = []
        add_image_list = []
        
        # TODO : atomic 구현
        if paper.user.id == user.id:
            paper.content          = data['condant']
            paper.x_axis           = data['x_axis']
            paper.y_axis           = data['y_axis']
            paper.background_color = data['background_color']
            paper.font             = data['font']
            paper.font_color       = data['font_color']
            paper.font_size        = data['font_size']
            
            paper.save()

            paper_images = Paper_image.objects.get(paper = paper)


            # 뺄 이미지
            for del_image in del_images:
                Paper_image.objects.get(image_url = del_image).delete()
            # 여기는 bulk delete 가 없어서 깡 delete 로 구현
            
            # 더할 이미지
            for image in images:
                image_url = self.image_upload(image)
                add_image_list.append(Paper_image(paper = paper, image_url = image_url))

            Paper_image.objects.bulk_create(add_image_list)
            
        else:
            return JsonResponse({'message' : 'permission denied'}, status = 400)

    # 페이지 삭제
    @login_decorator
    def delete(self, request):
        user = request.user
        data = json.loads(request.body)

        paper = Paper.objects.get(id = data['id'])
        if paper.user.id == user.id:
            paper.delete()
        else:
            return JsonResponse({'message' : 'permission denied'}, status = 400)

class PaperLikeView(View):
    # 좋아요 기능
    @login_decorator
    def post(self,request):
        user  = request.user
        data  = json.loads(request.body)
        paper = Paper.objects.get(id = data['paper_id'])

        paper_like, is_created =  Paper_Like.objects.get_or_create(user = user, paper = paper)

        if not is_created:
            paper_like.delete()
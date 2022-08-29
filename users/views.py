import requests 
import jwt
import boto3, uuid 

from datetime           import datetime, timedelta
from django.shortcuts   import redirect
from django.views       import View
from django.http        import JsonResponse, HttpResponse
from django.conf        import settings
from django.db          import transaction

from users.models import *
from utilities.logindecorator import login_decorator

class GoogleCallBackView(View): # 구글 인가 코드 발행.
    def __init__(self):
        self.google_auth_url    = "https://accounts.google.com/o/oauth2/v2/auth"
        self.access_token_uri   = "https://oauth2.googleapis.com/token"
        self.redirect_uri       = "http://127.0.0.1:8000/login/test"
        # self.redirect_uri       = "https://www.wemory.link/login/test"
        self.req_uri            = 'https://www.googleapis.com/oauth2/v3/userinfo'
        self.scope              = 'https://www.googleapis.com/auth/userinfo.profile + \
                                   https://www.googleapis.com/auth/userinfo.email'   # scope 여러 범위 설정하는 법.

    def get(self, request):
        
        return redirect(f"{self.google_auth_url}?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}")

    
class GoogleSignUpView(View): # 발행된 인가코드를 통해 access token 발행, 유저정보 요청
    def __init__(self):
        self.access_token_uri = "https://oauth2.googleapis.com/token"
        self.redirect_uri     = "http://127.0.0.1:8000/login/test"
        # self.redirect_uri     = "https://www.wemory.link/login/test"
        self.req_uri          = 'https://www.googleapis.com/oauth2/v3/userinfo'

    def get(self, request):
        code = request.GET.get("code")
        data = {
            "code"          : code,
            "client_id"     : settings.GOOGLE_CLIENT_ID,
            "client_secret" : settings.GOOGLE_CLIENT_PW ,
            "redirect_uri"  : self.redirect_uri,
            "grant_type"    : "authorization_code"
        }

        access_token = requests.post(self.access_token_uri, data = data).json()['access_token']
        
        headers      = {'Authorization': f'Bearer {access_token}'}

        user_info    = requests.get(self.req_uri , headers = headers).json()
        
        # get_or_created 구문을 사용하고 싶은데 아직 플래그에 대한 이해도가 낮음.
        # if 문을 통해 DB에서 이메일을 비교해 리스폰스 값을 바꿈
        # access token에 있는 이메일과 DB를 비교하여 이메일이 존재하면 웹페이지에서 사용할 토큰발급
        # 없다면 새로운 계정을 만들고 그에 대한 토큰을 발급.

        if User.objects.filter(google_email = user_info['email']).exists():
            user = User.objects.get(google_email = user_info['email'])
            
            login_token     =  jwt.encode({'user_id' : user.id, 'exp': datetime.utcnow() + timedelta(hours= 2)}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'Token' : login_token}, status = 200)
        
        else:
            new_user = User.objects.create(  
                name            = user_info['name'],
                google_email    = user_info['email'],
                profile_image   = user_info['picture'],
                ordinal         = Ordinal.objects.get(ordinal = 30),
                admin           = Admin.objects.get(title = '매니저')
                )
            
            login_token     =  jwt.encode({'user_id' : new_user.id, 'exp': datetime.utcnow() + timedelta(hours= 2)}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({'Token': login_token, 'message': '새로 가입'}, status = 200)
  

class ModifyView(View): # 토큰을 발급함. 토큰을 통해 유저 정보를 알아냄.
    def __init__(self):
        self.s3_connection = boto3.client(
            's3',
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        )
        self.profile_image_URL = "https://wemorys3.s3.ap-northeast-2.amazonaws.com/profile_image/"

    def image_upload(self, image):
        # 파일 업로드시 파일명이 겹칠 경우 s3 내에서 선입후출 (stack) 자료 구조로 
        # 파일을 자동 삭제한다고 한다. 그럴 경우를 방지하기 위해 uuid 를 사용한다.
        wemory_uuid = str(uuid.uuid4())
        self.s3_connection.upload_fileobj(
            image,
            "wemorys3",
            f'profile_image/{wemory_uuid}'
        )

        self.profile_image_URL = self.profile_image_URL + wemory_uuid
        
        return self.profile_image_URL
    
    @login_decorator
    def post(self, request):
        data = request.POST
        user = request.user
        
        try:
            with transaction.atomic():
            
                if "name" in data:
                    User.objects.filter(id = user.id).update(name = data['name'])
                
                elif "day_of_birth" in data:
                    User.objects.filter(id = user.id).update(day_of_birth = data['day_of_birth'])

                elif "ordinal" in data:
                    User.objects.filter(id = user.id).update(ordinal = data['ordinal']) 
                
                elif "profile_image" in data:
                    profile_image_file = request.FILES.__getitem__('image')
                    profile_image_URL = self.image_upload(profile_image_file)

                    User.objects.filter(id = user.id).update(profile_image = profile_image_URL) 
                    
                else:
                    return JsonResponse({'message' : 'No data contents to be modified.'}, status = 403)               

            check_values = list(User.objects.filter(id = user.id).values(
                "name",
                "ordinal",
                "day_of_birth",
                "profile_image"
            ))
            
            return JsonResponse({'message' : check_values }, status = 200)
        
        except:
            return JsonResponse({'message' : 'ModifyView Error' }, status = 404)
 


class CheckView(View): 
    def get(self, request):
        return HttpResponse('welcome')
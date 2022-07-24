import requests

from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.conf import settings


class GoogleCallBackView(View): # 구글 인가 코드 발행.
    def __init__(self):
        self.google_auth_url    = "https://accounts.google.com/o/oauth2/v2/auth"
        self.access_token_uri   = "https://oauth2.googleapis.com/token"
        self.redirect_uri       = "http://127.0.0.1:8080/login/test"
        self.req_uri            = 'https://www.googleapis.com/oauth2/v3/userinfo'
        self.scope              = 'https://www.googleapis.com/auth/userinfo.profile + \
                                   https://www.googleapis.com/auth/userinfo.email'   # scope 여러 범위 설정하는 법.

    def get(self, request):
        
        return redirect(f"{self.google_auth_url}?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}")

    
class GoogleAccessTokenView(View): # 발행된 인가코드를 통해 access token 발행, 유저정보 요청
    def __init__(self):
        self.access_token_uri = "https://oauth2.googleapis.com/token"
        self.redirect_uri     = "http://127.0.0.1:8080/login/test"
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

        return JsonResponse({'message' : user_info})




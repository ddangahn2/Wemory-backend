from lib2to3.pgen2 import token
import requests

from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.conf import settings



# Create your views here.

class WemoryView(View):
    def get(self):
        return JsonResponse({'message' : "get"})

    def post(self):
        return JsonResponse({'message' : "post"})    

class GoogleCallBackView(View):
    def __init__(self):
        # self.google_api_url = "https://oauth2.googleapis.com/token"
        self.google_client_id = "8257934324-ldhhmc031t5cpkluvd0gh9ghcfmmu4ku.apps.googleusercontent.com"
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.re = "http://127.0.0.1:8080/google/test"


    def get(self, request):

        return redirect(f"{self.google_auth_url}?client_id={self.google_client_id}&redirect_uri={self.re}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email")

class TestView(View):
    def get(self, request):
        access_token_uri = "https://oauth2.googleapis.com/token"
        code = request.GET.get("code")
        authorization_code = "authorization_code"
        data = {
            "code"          : code,
            "client_id"     : "8257934324-ldhhmc031t5cpkluvd0gh9ghcfmmu4ku.apps.googleusercontent.com",
            "client_secret" : "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" ,
            "redirect_uri"  : "http://127.0.0.1:8080/google/test",
            "grant_type"    : authorization_code
        }

        Test1 = requests.post(access_token_uri, data = data).json()['access_token']
        
        # print(dir(Test1))
        # print(Test1.json())
    
        req_uri      = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers      = {'Authorization': f'Bearer {Test1}'}

        user_info        = requests.get(req_uri , headers=headers).json()

        return JsonResponse({'message' : user_info})




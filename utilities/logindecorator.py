import jwt
import requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from wemory.settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            Token = request.headers.get('Authorization', None)
            payload      = jwt.decode(Token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = payload['user_id'])
            request.user = user
            

        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'INVALID_SIGNATURE_ERROR'}, status = 400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)

        
        return func(self, request, *args, **kwargs)
    return wrapper
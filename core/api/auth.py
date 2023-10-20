from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from core.models import User
from random import randint
from jose import jwt
import uuid
import datetime 


SECRET_KEY = settings.SECRET_KEY

class Otp():
    
    @staticmethod
    def send_otp(phone_number):
        code = randint(1000,9999)
        result = cache.get(phone_number)
        if not result:
           cache.set(key=phone_number,value=f"{code}",timeout=60 * 2,)
           print(code)
           return True
        else:
            return False # if phone number already in redis user should wait to ask again
        
    @staticmethod
    def check_otp(phone_number,code):
        result = cache.get(phone_number)
        return True if result == code else False
           

class Jwt():

    @staticmethod
    def create_jwt(user):
        token = jwt.encode({'user_id': user.id,"exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def get_user(token):
        try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
          user_id = payload.get('user_id') if payload else None
          user = User.objects.get(id=user_id)
        except:
            user = None
        return user
    


class ForgotPassword():

    def create_link(user):
        id = uuid.uuid4()
        phone_number = user.phone_number
        cache.set(key=f"{id}",value=phone_number,timeout=60 * 10,)
        print(id)
        return id
    
    def get_phone_number(uuid):
        phone_number = cache.get(uuid)
        print(phone_number)
        return phone_number if phone_number else None
    
    def send_link(uuid):
        pass


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.jwt = None
        try:
           header= request.headers['Authorization']
        except:
          header = None
        if header:
            auth_token = header.split(' ')[1]
            user =Jwt.get_user(auth_token)
            request.jwt = user if user else None                
        response =  self.get_response(request)
        return response
    

def login_required(view_func): #login required decorator for class methods
    def wrapper(self,request, *args, **kwargs):
        if not request.jwt:
            return Response(status=401)
        return view_func(self,request, *args, **kwargs) 
    return wrapper
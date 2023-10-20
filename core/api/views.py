from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from core.api.serializers import AskOtpSerializer,OtpLoginSerializer,ProfileSerializer,AddressSerializer,SignUpSerializer,LoginSerializer,PasswordChangeSerializer,ForgotPasswordSerializer
from core.models import User,Profile,Address
from core.api.auth import Otp,Jwt,login_required,ForgotPassword



class CreateOtp(APIView):

    def post(self,request):
        serializer = AskOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = Otp.send_otp(phone_number=serializer.validated_data['phone_number'])
            return Response(status=200) if result else Response("you have to wait to ask again",status=200)
        return Response(status=400)
    

class CheckOtp(APIView):

    def post(self,request):
        serializer = OtpLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            result = Otp.check_otp(phone_number=phone_number,code=serializer.validated_data['code'])
            user = User.objects.filter(phone_number=phone_number)
            if result and user :
                jwt = Jwt.create_jwt(user[0])
                return Response({"jwt":jwt},status=200)
            elif result:
                user = User(phone_number=phone_number)
                user.save()
                jwt = Jwt.create_jwt(user)
                return Response({"jwt":jwt},status=200)
        return Response("Invalid code",status=400)
    



class SignUpView(APIView):

    def post(self,request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User(phone_number = serializer.validated_data['phone_number'])
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response('user created',status=201)
        return Response(serializer.errors,status=400)

class LogInView(APIView):

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(phone_number = serializer.validated_data['phone_number'],password = serializer.validated_data['password'] )
            if user:
                jwt = Jwt.create_jwt(user)
                return Response({"jwt":jwt},status=200)
            return Response('incorrect phone number or password',status=400)
        return Response(serializer.errors,status=400)



class PasswordChangeView(APIView):

    @login_required
    def post(self,request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.jwt
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response('password changed',status=201)
        return Response(serializer.errors,status=400)
    

class ForgotPasswordLinkGeneratorView(APIView):

    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(phone_number = serializer.validated_data['phone_number'])
            ForgotPassword.create_link(user)
            return Response(status=200)
        return Response(serializer.errors,status=400)
    

class ChangePasswordUUIDView(APIView):

    def post(self,request,uuid):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = ForgotPassword.get_phone_number(uuid)
            if phone_number:
               user = User.objects.get(phone_number=phone_number)
               user.set_password(serializer.validated_data['password1'])
               user.save()
               return Response('password changed',status=201)
            return Response("link is timedout",status=408)
        return Response(serializer.errors,status=400)

class ProfileView(APIView):
    
    @login_required
    def get(self,request):
        try:
            profile = Profile.objects.get(user=request.jwt)
        except:
            profile = Profile(user=request.jwt)
            profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data,status=200)
    
    @login_required
    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = Profile.objects.get(user = request.jwt)
            profile.full_name = serializer.validated_data['full_name']
            profile.save()
            return Response("profile updated",status=201)
        return Response(status=400)
    


class AddressListView(APIView):
    
    @login_required
    def get(self,request):
        addreses = Address.objects.filter(user=request.jwt)
        serializer = AddressSerializer(addreses,many=True)
        return Response(serializer.data,status=200)
    @login_required    
    def post(self,request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.jwt)
            return Response("address added",status=201)
        return Response(status=400)
    
class AddressView(APIView):

    @login_required
    def get(self,request,id):
        try:
           address = Address.objects.get(id=id)
        except:
            return Response(status=404)
        if address.user == request.jwt:
           serializer = AddressSerializer(address)
           return Response(serializer.data,status=201)
        return Response(status=403)
        

    @login_required
    def delete(self,request,id):
        try:
           address = Address.objects.get(id=id)
        except:
            return Response(status=404)
        if address.user == request.jwt:
           address.delete()
           return Response("address deleted",status=201)
        return Response(status=403)
        
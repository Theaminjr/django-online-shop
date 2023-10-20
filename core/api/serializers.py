from rest_framework import serializers
from core.models import Profile,Address,User
from core.api.validators import password,phone_number

class AskOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators = [phone_number])

class OtpLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators = [phone_number])
    code = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, values):
        try:
            user = User.objects.get(phone_number=values['phone_number'])
        except:
            user = None           
        if not user:
            raise serializers.ValidationError("user does not exist")
        return values
    
class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators = [phone_number])
    password1 = serializers.CharField(validators = [password])
    password2 = serializers.CharField(validators = [])

    def validate(self, values):
        try:
            user = User.objects.get(phone_number=values['phone_number'])
        except:
            user = None           
        if user:
            raise serializers.ValidationError("phone number already exists")
        if not values['password1'] == values['password2']:
            raise serializers.ValidationError("passwords does not match")
        return values
 
class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(validators = [password])
    password2 = serializers.CharField(validators = [])

    def validate(self, values):
        if not values['password1'] == values['password2']:
            raise serializers.ValidationError("passwords does not match")
        return values


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    def validate(self, values):
        try:
            user = User.objects.get(phone_number=values['phone_number'])
        except:
            user = None           
        if not user:
            raise serializers.ValidationError("user does not exist")
        return values

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id',"postal_code","text"]


# get phone_number
# create otp
# send otp
# check if otp correct
# create user
# create jwt
# check jwt

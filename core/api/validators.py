from rest_framework import serializers
import re




def phone_number(value):
    if len(value) <11:
        raise serializers.ValidationError("phone number is invalid.")

def password(value):
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', value):
       raise serializers.ValidationError('password must be at minimum 8 characters,including at least one letter and one number.')
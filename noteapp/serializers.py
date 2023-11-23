from rest_framework import serializers
from .models import User,Note
from django.core.exceptions import ValidationError
import re

class PasswordValidator:
    def __call__(self, value):
        if len(value) < 6 or len(value) > 14:
            raise ValidationError("Password must be between 6 and 14 characters")

        if not re.search("[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search("[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search("[0-9]", value):
            raise ValidationError("Password must contain at least one digit")

        if not re.search("[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("Password must contain at least one special character")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=True,validators=[PasswordValidator()],style={'input_type': 'password'}
    )
    class Meta:
        model=User
        fields=['email','firstname','lastname','password','password2']
        extra_kwargs={'password':{'write_only':True}}
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password adn confirm password doesn't match ")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields=['title', 'content', 'created_at', 'updated_at', 'user']
   
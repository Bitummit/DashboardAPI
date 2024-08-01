from rest_framework import serializers
from .models import User
import re
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from rest_framework.validators import UniqueValidator


# class UserSerializer(serializers.Serializer):
#     '''Method to understand Serializer'''

#     email = serializers.EmailField()
#     login = serializers.CharField(max_length=64)
#     image = serializers.ImageField()
#     phone = serializers.CharField(max_length=12)
#     country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
#     created_at = serializers.DateTimeField()

#     def create(self, validated_data):
#         return User.objects.create(**validated_data)

    # def update(self, instance, validated_data):

    #     instance.email = validated_data.get('email', instance.email)
    #     instance.login = validated_data.get('login', instance.login)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.created_at = validated_data.get('created_at', instance.created_at)
    #     instance.save()
    #     return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class BaseUserSerializer(serializers.ModelSerializer):
    '''Users List'''
    balance = serializers.ReadOnlyField(source="wallet.balance")
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "image", "phone", "country", "status", "balance", "created_at"]

    def validate_phone(self, value):
        validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
        if re.match(validate_phone_number_pattern, value):
            return value
        raise serializers.ValidationError("Phone number don't match the pattern")


class ShortUserSerializer(BaseUserSerializer):
    '''Only POST'''

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "phone", "password"]

'''
Sign in ("email", "username", "phone", "password")
Sign up ()
Get users ("email", "username", "image", "phone", "country", "created_at")
Create user ()

User email username password iamge phone country created at
'''
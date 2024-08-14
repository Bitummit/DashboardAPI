from rest_framework import serializers
from .models import User, Wallet, Transaction, TokenInWallet
import re
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from rest_framework.validators import UniqueValidator
from django.db import transaction


class BaseUserSerializer(serializers.ModelSerializer):
    '''Users List'''
    balance = serializers.ReadOnlyField(source="wallet.balance")
    class Meta:
        model = User
        fields = ["pk", "first_name", "last_name", "email", "username", "image", "phone", "country", "status", "balance", "created_at"]

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


class TransactionSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=5)
    user_to = serializers.CharField(max_length=64)

    class Meta:
        model = Transaction
        fields = ["user_to", "token", "amount"]

    def validate(self, data):
        user_from = self.context['request'].user
        
        if not user_from:
            raise serializers.ValidationError({"user_from": "Not authenticated!"})

        user_to = User.objects.filter(username=data["user_to"]).first()
        if not user_to:
            raise serializers.ValidationError({"user_to": "No such user!"})
        
        token = user_from.wallet.tokens.filter(token__short_name=data["token"])
        if not token:
            raise serializers.ValidationError({"token": "User don't have such token!"})
        
        if data["amount"] < 0:
            raise serializers.ValidationError({"amount": "Amount can't be less then 0!"})
        elif data["amount"] > token.amount:
            raise serializers.ValidationError({"amount": "User don't have such amount!"})

        return data

    def create(self, validated_data):
        with transaction.atomic():
            pass

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", 'email', "country", 'password', 'password2']

    # def validate_phone(self, value):
    #     validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    #     if re.match(validate_phone_number_pattern, value):
    #         return value
    #     raise serializers.ValidationError("Phone number don't match the pattern")
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Wallet.objects.create(user=user)
        return user


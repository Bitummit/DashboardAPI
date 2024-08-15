import re
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import (
    User,
    Wallet, 
    Transaction,
    Token
)



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


class TransactionSerializer(serializers.Serializer):
    '''Transaction operation'''
    user_to = serializers.CharField(max_length=64)
    token = serializers.CharField(max_length=5)
    amount = serializers.DecimalField(max_digits=20, decimal_places=10)

    def validate(self, attrs):
        user_from = self.context['request'].user
        
        if not user_from:
            raise serializers.ValidationError({"user_from": "Not authenticated!"})
        try:
            user_to = User.objects.get(username=attrs["user_to"])
        except Exception:
            raise serializers.ValidationError({"user_to": "No such user!"})
        
        try:
            token = user_from.wallet.tokens.get(token__short_name=attrs["token"])
        except Exception:
            raise serializers.ValidationError({"token": "User don't have such token!"})
        
        if attrs["amount"] < 0:
            raise serializers.ValidationError({"amount": "Amount can't be less then 0!"})
        elif attrs["amount"] > token.amount:
            raise serializers.ValidationError({"amount": "User don't have such amount!"})

        return attrs

    def create(self, validated_data):
        '''Make users and token fileds from another Srializer'''
        user_from = self.context['request'].user
        user_to = User.objects.get(username=validated_data["user_to"])
        token_base = Token.objects.get(short_name=validated_data["token"])
        new_transaction = Transaction.objects.create(user_from=user_from, user_to=user_to, amount=validated_data["amount"])

        try:
            with transaction.atomic():
                token_user_from = user_from.wallet.tokens.get(token=token_base)
                token_user_from.amount -= validated_data["amount"]
                token_user_from.save()
                token_user_to, created = user_to.wallet.tokens.get_or_create(token=token_base, wallet=user_to.wallet)
                token_user_to.amount += validated_data["amount"]
                token_user_to.save()

                new_transaction.status = "Completed"
                new_transaction.save()
        except Exception:
            new_transaction.status = "Canceled"
            new_transaction.save()

        return new_transaction
    


# class TokenSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Token
#         fields = '__all__'
            

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''Token get view'''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    '''User registration view'''
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


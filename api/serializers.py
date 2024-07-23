from rest_framework import serializers
from .models import User, COUNTRY_CHOICES
import re

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
        raise serializers.ValidationError("Phone number don't match teh pattern")


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
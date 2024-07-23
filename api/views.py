from django.shortcuts import render
from rest_framework import generics, pagination
from .models import User
from .serializers import BaseUserSerializer, ShortUserSerializer
from .services import StandardPagination

'''
users list
tokens get
wallet get
transactions get
jwt
user post
'''

class UserListView(generics.ListCreateAPIView):
    '''ListCreate'''
    serializer_class = ShortUserSerializer
    queryset = User.objects.filter(is_staff=False).all()
    pagination_class = StandardPagination
    # pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BaseUserSerializer
        return self.serializer_class



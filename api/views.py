from django.shortcuts import render
from rest_framework import generics, pagination
from .models import User
from .serializers import BaseUserSerializer, ShortUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from .services import StandardPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
import time
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
    queryset = User.objects.filter(is_staff=False).all().order_by('pk')
    pagination_class = StandardPagination
    # pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            # time.sleep(2)
            return BaseUserSerializer
        return self.serializer_class

    ''' Create wallet auto adding'''


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



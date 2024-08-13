from django.shortcuts import render
from rest_framework import generics, pagination, filters
from .filters import MyCustomOrdering
from .models import User
from .serializers import BaseUserSerializer, ShortUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from .services import StandardPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
import time

'''
users list - done
tokens get
wallet get
transactions get
jwt - done
user post - done
'''

class UserListView(generics.ListAPIView):
    '''ListCreate'''
    serializer_class = ShortUserSerializer
    queryset = User.objects.filter(is_staff=False).all().select_related("wallet")
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["pk", "last_name", "email", "wallet__balance", "status"]
    ordering = ['-pk']
    # pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            # time.sleep(2)
            return BaseUserSerializer
        return self.serializer_class


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


'''
Update token price with celery -> create tokenHistory entity -> update token
'''
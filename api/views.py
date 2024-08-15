from django.shortcuts import render
from rest_framework import generics, pagination, filters
from .filters import MyCustomOrdering
from .models import User, Transaction
from .serializers import TransactionSerializer, BaseUserSerializer, ShortUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from .paginators import StandardPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
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


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated, )


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
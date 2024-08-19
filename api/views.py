from django.shortcuts import render
from rest_framework import generics, pagination, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
import time

from .filters import MyCustomOrdering
from .models import User, Transaction, TokenInWallet
from .serializers import (
    TransactionSerializer,
    BaseUserSerializer, 
    ShortUserSerializer, 
    MyTokenObtainPairSerializer, 
    RegisterSerializer,
    TokenInWalletSerializer
)
from .paginators import StandardPagination


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
    serializer_class = BaseUserSerializer
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


class CreateTokenInWallet(generics.ListCreateAPIView):
    serializer_class = TokenInWalletSerializer
    queryset = TokenInWallet.objects.all()
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = TokenInWallet.objects.select_related("wallet", "wallet__user").filter(wallet__user=request.user)
        serializer = TokenInWalletSerializer(queryset, many=True)
        return Response(serializer.data)
    

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
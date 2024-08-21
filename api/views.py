from django.shortcuts import render
from rest_framework import generics, pagination, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
import time
from django.db.models import Q

from .filters import MyCustomOrdering
from .models import User, Transaction, TokenInWallet, Wallet
from .serializers import (
    TransactionSerializer,
    BaseUserSerializer, 
    ShortUserSerializer, 
    MyTokenObtainPairSerializer, 
    RegisterSerializer,
    TokenInWalletSerializer,
    WalletSerializer
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

    serializer_class = BaseUserSerializer
    queryset = User.objects.filter(is_staff=False).all().select_related("wallet")
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["pk", "last_name", "email", "wallet__balance", "status"]
    ordering = ['-pk']
    # pagination_class = pagination.LimitOffsetPagination


class TransactionListCreateView(generics.ListCreateAPIView):

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        print(request.user)
        queryset = Transaction.objects.select_related("user_from", "user_to").filter(Q(user_to=request.user) | Q(user_from=request.user)).order_by("-pk").all()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CreateTokenInWalletView(generics.ListCreateAPIView):

    serializer_class = TokenInWalletSerializer
    queryset = TokenInWallet.objects.all()
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = TokenInWallet.objects.select_related("wallet", "wallet__user").filter(wallet__user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetriveBalanceView(generics.RetrieveAPIView):

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, )


class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


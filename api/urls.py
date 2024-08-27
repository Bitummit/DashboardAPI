from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,TokenObtainPairView
)


urlpatterns = [
    path('users/', views.UserListView.as_view(), name="users"),
    path('jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('token/', views.CreateTokenInWalletView.as_view(), name="add_balance"),
    path('wallet/<int:pk>', views.RetriveBalanceView.as_view(), name="show_balance"),

    path('transaction/', views.TransactionListCreateView.as_view(), name='transaction'),
]

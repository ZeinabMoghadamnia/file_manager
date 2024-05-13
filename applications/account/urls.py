from django.urls import path, include
from .views import CustomLoginView, CustomLogoutView, RegisterView, ActivateAccountView, SendOTPCodeView, VerifyOTPView, \
    CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('activate/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('send_otp/', SendOTPCodeView.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('panel/', include('apps.accounts.API.urls')),

]

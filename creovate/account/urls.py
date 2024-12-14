from tkinter.font import names

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from django.contrib.auth import views as auth_views

from creovate.account.views import RegisterViewCustomer, HomeView, ProfileLoginViewCustomer, ProfileLoginViewFreelancer, \
    RegisterViewFreelancer, FreelanceHomeView, ForgotPasswordView, PasswordResetView, ProfilePageView, \
    UpdateProfileView, ProfileFreelancePageView, UpdateProfileFreelanceView, DeleteAccountView, WalletViewCustomer, \
    UpdateWalletViewCustomer, CheckOutView, HistoryView, CancelOrderView, WalletViewFreelancer, \
    UpdateWalletViewFreelancer, OrderListFreelancerView, DetailOrderListView

urlpatterns = [
    path('home/', include([
        path('', HomeView.as_view(), name='home'),
        path('profile/<str:username>/', ProfilePageView.as_view(), name='profile'),
        path('update-profile/<str:username>/', UpdateProfileView.as_view(), name='update_profile'),
        path('Creovate-wallet/<str:username>/', WalletViewCustomer.as_view(), name='customer_wallet'),
        path('update-wallet/<str:username>', UpdateWalletViewCustomer.as_view(), name='update_wallet_customer'),
        path('delete-profile/<int:pk>', DeleteAccountView.as_view(), name='delete_profile'),
    ])),

    path('freelance-homepage/', include([
        path('', FreelanceHomeView.as_view(), name='freelance_homepage'),
        path('profile/<str:username>/', ProfileFreelancePageView.as_view(), name='profile_freelance'),
        path('update-profile/<str:username>/', UpdateProfileFreelanceView.as_view(), name='update_profile_freelance'),
        path('Creovate-wallet/<str:username>/', WalletViewFreelancer.as_view(), name='freelancer_wallet'),
        path('update-wallet/<str:username>', UpdateWalletViewFreelancer.as_view(), name='update_wallet_freelancer'),
        path('history-list/', OrderListFreelancerView.as_view(), name='history_list_freelancer'),
        path('history-list/<int:pk>/', DetailOrderListView.as_view(), name='history_list_customer'),

    ])),

    path('login/', ProfileLoginViewCustomer.as_view(), name='login'),
    path('loginFreelance/', ProfileLoginViewFreelancer.as_view(), name='loginFreelance'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registerFreelance/', RegisterViewFreelancer.as_view(), name='registerFreelance'),
    path('register/', RegisterViewCustomer.as_view(), name='register'),

    path('checkout_service/<int:service_id>', CheckOutView.as_view(), name='checkout_service'),
    path('history_order/<str:username>/', HistoryView.as_view(), name='history_order'),
    path('cancel_order/<int:order_id>/cancel', CancelOrderView.as_view(), name='cancel_order'),

    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('reset_password/', ForgotPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="resetPassword/reset_password_message.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetPassword/reset_password_success.html'), name='password_reset_complete'),

]
from django.urls import path
from accounts.api.views import (TransactionDetail, TransactionDetailUser, TransactionList,
                                RegistrationView, EmailRegistrationVerificationView, ActivateAccountView)
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('list-admin/', TransactionList.as_view(), name='transaction_list_admin'),
    path('detail-admin/<int:pk>', TransactionDetail.as_view(), name='transaction_detail_admin'),
    path('detail/<int:pk>', TransactionDetailUser.as_view(), name='transaction_detail_user'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('email-registration/', EmailRegistrationVerificationView.as_view(), name='email_registration'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="reset_pass/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="reset_pass/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="reset_pass/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="reset_pass/password_reset_done.html"), 
        name="password_reset_complete"),

]

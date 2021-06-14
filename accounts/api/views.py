from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateAPIView

from accounts.models import NewUser, TestTransaction
from accounts.api.serializers import TestTransactionSerializer, RegistrationSerializer

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.api.permissions import IsTransactionUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.custom_email import activation_email

class TransactionList(ListAPIView):
    queryset = TestTransaction.objects.all()
    serializer_class = TestTransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class TransactionDetail(RetrieveUpdateAPIView):
    queryset = TestTransaction.objects.all()
    serializer_class = TestTransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# for end user, user can edit only its transaction model
class TransactionDetailUser(RetrieveUpdateAPIView):
    queryset = TestTransaction.objects.all()
    serializer_class = TestTransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTransactionUser, IsAuthenticated]

# direct registration and activation
class RegistrationView(CreateAPIView):
    queryset = NewUser.objects.all()
    serializer_class = RegistrationSerializer

# registration and then email verification for activation
class EmailRegistrationVerificationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = NewUser.objects.get(user_name = serializer.validated_data['user_name'])
            current_site = get_current_site(request)
            domain = current_site.domain
            token = PasswordResetTokenGenerator().make_token(user)
            activation_email(user.user_name, domain, user.pk, token, user.email)
            return Response({'registered':'please go to your email and verify'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(GenericAPIView):

    def get(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = NewUser.objects.get(pk=uid)
        except Exception:
            user = None
        if user is not None and PasswordResetTokenGenerator().check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            return HttpResponse('You are now activated, you can be authenticated')
        return HttpResponse('not activated')
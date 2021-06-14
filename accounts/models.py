from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    options = (
        ('none', 'None'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    )

    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(10), 
                                        MaxValueValidator(110)], null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=options, default='none')
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]

    def __str__(self):
        return self.user_name

class TestTransaction(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=50, null=True, blank=True, default='Delhi')

    def __str__(self):
        return f'{self.user} | {self.location}'

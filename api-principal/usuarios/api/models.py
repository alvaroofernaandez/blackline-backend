from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrador'),
        (USER, 'Usuario normal')
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Correo electrónico")
    can_receive_emails = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=False, verbose_name="Contraseña")
    instagram_username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección")
    nif = models.CharField(max_length=20, null=True, blank=True, verbose_name="NIF")
    role = models.CharField(max_length=10, choices=ROLES, default=USER)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'role']

    def clean(self):

        content = [self.username, self.email]
        if not all(content):
            raise ValidationError("Todos los campos deben de estar rellenos")

    def __str__(self):
        return self.username or self.email

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Municipality(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")

    class Meta:
        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    document_number = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^\d+$', 'Solo se permiten números.')],
        verbose_name="Document Number"
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name="Phone")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['document_number']

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255, verbose_name="Street")
    neighborhood = models.CharField(max_length=100, verbose_name="Neighborhood")
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, related_name='addresses', null=True)
    reference = models.TextField(blank=True, verbose_name="Reference")

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.neighborhood}, {self.municipality.name if self.municipality else ''}"
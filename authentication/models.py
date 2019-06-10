import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        if not first_name or not last_name:
            raise ValueError("First name or Last name is required")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        return self._create_user(email, password, first_name, last_name, is_active=True, is_staff=False,
                                 is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        return self._create_user(email, password, first_name, last_name, is_active=True, is_staff=True,
                                 is_superuser=True, **extra_fields)


def custom_upload_url(instance, _filename):
    return "dps/{}.jpg".format(instance.pk)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.CharField(max_length=128, verbose_name="Email", unique=True)
    password = models.CharField(max_length=12, verbose_name="Password")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    image = models.ImageField(upload_to=custom_upload_url, null=True, blank=True, default='dps/profile.jpg')
    friends = models.ManyToManyField(to="self")
    city = models.CharField(null=True, blank=True, default='', max_length=150)
    country = models.CharField(null=True, blank=True, default='', max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    notifications = models.ManyToManyField('core.Notification')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, default='male')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

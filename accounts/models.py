from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserManager(BaseUserManager):

    # Create a regular user
    def create_user(self, email, password, **extra_fields):

        # normalize the email into a format acceptable by Django
        email=self.normalize_email(email)

        # set the email field equal to a normalized email
        user=self.model(
            email=email,
            **extra_fields
        )

        # use set_password to hash the password
        user.set_password(password)

        # save the user
        user.save()

        # return the user
        return user
    
    # Create a super user
    def create_superuser(self, email, password, **extra_fields):

        # Require the user attributes 'is_staff' and 'is_superuser' to True
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("if_staff") is not True:
            raise ValueError("Superuser has to have is_staff set equal to True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser set equal to True")
        
        # Return the created super user
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):

    # these are additional specifications we would like to make to the default User model provided bny Django
    email = models.CharField(max_length=80, unique=True)
    username=models.CharField(max_length=45, unique=True)
    date_of_birth=models.DateField(null=True)

    # a custom manager defined above for creating our users
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

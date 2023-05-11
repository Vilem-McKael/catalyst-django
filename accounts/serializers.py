from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import User

# Allows the conversion of object data into native Python datatypes
# That can then be rendered to and from JSON
class SignUpSerializer(serializers.ModelSerializer):

    # ensures that incoming and outgoing User data follows the standards
    # set in our User models
    email=serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=45)
    password=serializers.CharField(min_length=8, write_only=True)

    # Meta determines which User fields will be accessible from our API calls
    class Meta:
        model=User
        fields=['email', 'username', 'password']

    # Used when creating a user to ensure that the email and username do not exist in the database.
    # Takes in serialized user data from a sign-up request
    def validate(self, attrs):

        # Filter through the database to check if the email or username exist, i.e. have previously been created
        email_exists = User.objects.filter(email=attrs['email']).exists()
        # username_exists = User.objects.filter(username=attrs['username']).exists()

        # If either the email or username are already in the database, raise an error
        if email_exists: #or username_exists
            raise ValidationError("Email has already been used to create an account")
        
        # Returns the result of validating the "superclass" of our custom user, aka the Django User model
        return super().validate(attrs)
    
    # An middle function to ensure that created users have a hashed password and an associated Token
    def create(self, validated_data):
        
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user
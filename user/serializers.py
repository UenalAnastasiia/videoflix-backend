from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from user.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """"
    Serialiser for registering a new user object in the user database.
    """
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    image = serializers.CharField(max_length=500)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password_repeat', 'email', 'first_name', 'last_name', 'image')

    def validate(self, attrs):
        """"
        Validates that both password fields match.
        """
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from user.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """"
    Register new User Object in Users DB
    """
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password_repeat', 'email', 'first_name', 'last_name')


    def validate(self, attrs):
        """"
        Check def if both password fields match
        """
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    def create(self, validated_data):
        """"
        Create new User Object in System with validated data
        """
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.save()
        return user
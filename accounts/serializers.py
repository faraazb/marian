from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # this ensures client cannot send a token while signing up
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number',)


class UserLoginRestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number',)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token', 'first_name', 'last_name', 'email', 'phone_number',)
        extra_kwargs = {'first_name': {'required': False}, 'email': {'required': False},
                        'phone_number': {'required': False}}

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        if username is None:
            raise serializers.ValidationError("Username is required to login")
        if password is None:
            raise serializers.ValidationError("Password is required to login")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("User with this username and password was not found")
        if not user.is_active:
            raise serializers.ValidationError("Account has been deactivated")

        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'token': user.token
        }

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is taken!')

        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('E-mail is taken!')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                        password=validated_data['password'])
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is incorrect!')

        elif not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('E-mail is incorrect!')

        return data

    def get_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {
                'data': {},
                'message': 'Invalid credentials!'
            }

        refresh = (RefreshToken.for_user(user))
        return {'data': {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }, 'message': 'Login Successful!'}

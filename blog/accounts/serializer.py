from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
        return tokens


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
            return None

        refresh = (RefreshToken.for_user(user))
        tokens = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
        return tokens


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_email(self, value):
        user = self.context['request'].user
        if value != user.email:
            raise serializers.ValidationError("Invalid email for the provided token.")
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect!")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

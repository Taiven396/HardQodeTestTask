from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def validate(self, data):
        super().validate(data)
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        try:
            User.objects.get(username=validated_data['username'])
            return False
        except User.DoesNotExist:
            user = User.objects.create_user(username=validated_data['username'])
            user.set_password(validated_data['password'])
            user.save()
            profile = UserProfile(user=user, status='Новый')
            profile.save()
            return user


class LoginSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['username', 'password']

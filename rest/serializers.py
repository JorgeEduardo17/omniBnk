from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Movies

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    attrs['error'] = {'code':1,'description':'User account is disabled.'}
            else:
                attrs['error'] = {'code': 2, 'description': 'Unable to log in with provided credentials.'}
        else:
            attrs['error'] = {'code': 3, 'description': 'Must include "email" and "password".'}

        attrs['user'] = user
        return attrs

class MoviesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('title', 'rating', 'fav')

    def create(self, validated_data):
        movie = Movies.objects.create(**validated_data, user=User.objects.get(id=self.context['user_id']))
        return movie

class MoviesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('id', 'creation','title', 'rating', 'fav')
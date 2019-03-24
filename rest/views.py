# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest import serializers
from rest_framework import mixins
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import Movies

# Create your views here.

class SignUpView(mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    Vista que maneja el registro de usuario, se requieren los siguientes parametros:

    title
    rating
    fav

    """
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ObtainAuthToken(APIView):

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = serializers.AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data_return = {}
        if user == None:
            data_return['token'] = None
            data_return['error'] = serializer.validated_data['error']
        else:
            token, created = Token.objects.get_or_create(user=user)
            data_return['token'] = token.key
            data_return['error'] = None
        return Response(data_return)


class RemoveAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class MoviesApiView(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    generics.GenericAPIView):

    def get_serializer_class(self):

        """
        Este metodo sobreescribe la selección del serializador en función del metodo usado para acceder al endpoint.
        """

        serializer_class = None
        if self.request.method == 'GET':
            serializer_class = serializers.MoviesListSerializer
        elif self.request.method == 'POST':
            serializer_class = serializers.MoviesCreateSerializer
        return serializer_class

    def get_queryset(self):
        """
        Se filtra la query para que solo se pueda acceder a las peliculas del usuario que proporciona las credenciales.
        """
        return Movies.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_serializer_context(self):
        """
        Este metodo envia al contexto del serializador el id del usuario que proporciona las credenciales.
        """
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        object = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializers.MoviesListSerializer(object).data, status=status.HTTP_201_CREATED, headers=headers)

class MovieApiView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):

    def get_queryset(self):
        return Movies.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_class = None
        if self.request.method == 'GET':
            serializer_class = serializers.MoviesListSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = serializers.MoviesCreateSerializer
        return serializer_class

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        data = serializers.MoviesListSerializer(Movies.objects.get(id=kwargs['pk'])).data
        return Response(data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class MovieFavListApiView(mixins.ListModelMixin,
                          generics.GenericAPIView):

    serializer_class = serializers.MoviesListSerializer

    def get_queryset(self):
        return Movies.objects.filter(user=self.request.user,fav = True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
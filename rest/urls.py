from django.urls import path, include
from rest.views import SignUpView, ObtainAuthToken, RemoveAuthToken, MoviesApiView, MovieApiView, MovieFavListApiView

app_name = 'rest'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('get_auth_token/', ObtainAuthToken.as_view()),
    path('remove_auth_token/', RemoveAuthToken.as_view()),
    path('movies/', MoviesApiView.as_view()),
    path('movies/<int:pk>/', MovieApiView.as_view()),
    path('movies/fav/', MovieFavListApiView.as_view())
]
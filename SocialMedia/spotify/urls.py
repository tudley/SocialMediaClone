from django.urls import path

from . import views
app_name = 'spotify'

urlpatterns = [

    # home page explaining the Spotify app
    path('home/', views.home, name='home'),

    # search page, allowing users to search in spotifys database
    path('search/', views.search, name='search')

]
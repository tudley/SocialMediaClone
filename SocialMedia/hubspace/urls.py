from django.urls import path

from . import views
app_name = 'hubspace'

urlpatterns = [

    # page showing all the users in the database
    path("users/", views.users, name='users'),

    # page of an individual user
    # eg localhost:8000/hub/profile/12
    path("profile/<int:id>/", views.profile_page, name='profile_page'),
    
    # page of adding a new post
    # eg localhost:8000/hub/profile/12/new_post
    path('profile/<int:id>/new_post', views.new_post, name = 'new_post'),

    # page of adding a comment to a post
    # eg localhost:8000/hub/post/<int:post_id>/new_comment
    path('profile/<int:profile_id>/post/<int:post_id>/comment', views.new_comment, name = 'new_comment'),
    
    # this path gets called on successful login, and redirects to profile.
    path('profile/', views.redirect_to_profile, name = 'redirect_to_profile'),

    # redirect user back to profile of <int:id> after following the profile
    path('profile/<int:profile_id>/follow', views.follow_profile, name = 'follow_profile'),

    # redirect user back to profile of <int:id> after following the profile
    path('profile/<int:profile_id>/unfollow', views.unfollow_profile, name = 'unfollow_profile'),

]
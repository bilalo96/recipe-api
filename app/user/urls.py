"""URL mappings for the User Api"""
from django.urls import path
from user import views

app_name='user' # this app name use for reverse mapping that we deffined in test user api

urlpatterns = [
    path('create/',views.CreateUserView.as_view(),name='create')
]


from django.urls import path

from . import views

app_name = 'slashcommands'
urlpatterns = [
    path('', views.auth, name='auth'),
]

from django.urls import path

from . import views

app_name = 'slashoauth'
urlpatterns = [
    path('', views.auth, name='auth'),
]

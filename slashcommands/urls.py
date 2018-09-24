from django.urls import path

from . import views

app_name = 'slashcommands'
urlpatterns = [
    path('walkup', views.walkup, name='walkup'),
    path('gsheet', views.gsheet_test, name='test'),
]

from django.contrib import admin
from django.urls import path
from log_analysis import views

urlpatterns = [
    path('', views.index, name='log_analysis'),  # Root path should point to index view with name 'log_analysis'
    path('login', views.login, name='login'),  # Login path with trailing slash
    path('logout', views.logout_view, name='logout_view'),  # Logout path with trailing slash
]

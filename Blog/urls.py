from django.urls import path
from .views import main, users, write

urlpatterns = [
    path('', main, name='main'),
    path('users', users, name='users'),
    path('write', write, name='write'),
]

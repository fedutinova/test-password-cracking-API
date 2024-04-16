from django.urls import path
from . import views

app_name = 'authorization'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('test_token', views.test_token, name='test_token')
]
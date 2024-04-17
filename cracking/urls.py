from django.urls import path
from .views import crack_md5_hash, crack_history

urlpatterns = [
    path('crack', crack_md5_hash, name='crack_md5_hash'),
    path('history', crack_history, name='crack_history'),
]
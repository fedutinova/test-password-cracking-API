from django.urls import path
from .views import crack_md5_hash, view_submission_history

urlpatterns = [
    path('crack', crack_md5_hash, name='crack_md5_hash'),
    path('history', view_submission_history, name='view_submission_history'),
]
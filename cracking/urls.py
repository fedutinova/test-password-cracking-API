from django.urls import path
from .views import submit_md5_hash, view_submission_history

urlpatterns = [
    path('submit', submit_md5_hash, name='submit_md5_hash'),
    path('history', view_submission_history, name='view_submission_history'),
]
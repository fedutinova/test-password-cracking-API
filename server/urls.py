from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls'), name='authorization'),
    path('cracking/', include('cracking.urls'), name='cracking'),
]

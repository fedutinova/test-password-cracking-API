from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('cracking/', include('cracking.urls')),
]

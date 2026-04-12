from django.urls import path
from .views import home, anonymize_api

urlpatterns = [
    path('', home, name='home'),
    path('api/', anonymize_api, name='api_anonymize'),
]

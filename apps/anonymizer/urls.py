from django.urls import path
from .views import home, anonymize_api, api_docs

urlpatterns = [
    path('', home, name='home'),
    path('api/', anonymize_api, name='api_anonymize'),
    path('api-docs/', api_docs, name='api_docs'),
]

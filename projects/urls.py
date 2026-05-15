from django.urls import path
from .views import get_projects, create_contact

urlpatterns = [
    path('projects/', get_projects),
    path('contact/', create_contact),
]
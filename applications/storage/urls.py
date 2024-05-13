from django.urls import path, include
from .views import HomeView

app_name = 'storage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]

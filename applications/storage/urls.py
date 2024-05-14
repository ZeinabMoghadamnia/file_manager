from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import FileListView, DeleteView
# from .views import HomeView
from applications.storage.views import FileListView, DeleteView
from applications.storage.views import HomeView

app_name = "storage"
urlpatterns = [
    path("", FileListView.as_view(), name="file-list"),
    path("file/delete/<int:file_id>/", DeleteView.as_view(), name="delete"),
]

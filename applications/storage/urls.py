from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import FileListView, DeleteView
# from .views import HomeView
from applications.storage.views import FileListView, DeleteView, HomeView, FileUploadView

app_name = "storage"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("storage/", FileListView.as_view(), name="file-list"),
    path("file/delete/<int:file_id>/", DeleteView.as_view(), name="delete"),
    path("upload/", FileUploadView.as_view(), name="upload"),
]

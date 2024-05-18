from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import FileListView, DeleteView
# from .views import HomeView
from applications.storage.views import (
    FileListView,
    DeleteFileView,
    FileUploadView,
    FolderListView,
    DeleteFolderView,
    FolderDetails,
    DownloadFileView,
    DownloadFolderView,
    FolderAndFilesView,
    CreateFolderView,
    FileContentView,
    FileFolderSearchView,
    EditFileView,
    EditFolderView,
)

app_name = "storage"
urlpatterns = [
    path("storage/", FolderAndFilesView.as_view(), name="storage"),
    path("files/", FileListView.as_view(), name="file-list"),
    path("file/delete/<int:file_id>/", DeleteFileView.as_view(), name="delete-file"),
    path("upload/", FileUploadView.as_view(), name="upload-file"),
    path("folders/", FolderListView.as_view(), name="folders-list"),
    path(
        "folder/delete/<int:folder_id>/",
        DeleteFolderView.as_view(),
        name="delete-folder",
    ),
    path("create/", CreateFolderView.as_view(), name="create-folder"),
    path("folder/detail/<int:pk>/", FolderDetails.as_view(), name="folder-files"),
    path("file/<int:file_id>/", FileContentView.as_view(), name="file_content_view"),
    path("download/<int:file_id>/", DownloadFileView.as_view(), name="download-file"),
    path(
        "download-folder/<int:folder_id>/",
        DownloadFolderView.as_view(),
        name="download-folder",
    ),
    path("search/", FileFolderSearchView.as_view(), name="file-folder-search"),
    path("edit/<int:id>/file/", EditFileView.as_view(), name="edit-files"),
    path("edit/<int:id>/folder/", EditFolderView.as_view(), name="edit-folders"),
]

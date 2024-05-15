from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

# from .models import File
from applications.storage.models import File, Folder

# from .forms import FileUploadForm
from applications.storage.forms import FileUploadForm
from rest_framework.permissions import AllowAny, IsAuthenticated

# from .serializers import FileSerializer
from applications.storage.serializers import FileSerializer, UploadFileSerializer, FolderSerializer, CreateFolderSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class FileListView(ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return render(request, "storage.html", {"files": serializer.data})

class FolderListView(ListAPIView):
    serializer_class = FolderSerializer

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return render(request, "folders.html", {"folders": serializer.data})


class DeleteFileView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user_files = File.objects.filter(user=request.user)
            for file in user_files:
                if file.id == kwargs.get("file_id"):
                    file.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Item not found or unable to delete"},
            status=status.HTTP_404_NOT_FOUND,
        )
        
class DeleteFolderView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user_folders = Folder.objects.filter(user=request.user)
            for folder in user_folders:
                if folder.id == kwargs.get("folder_id"):
                    folder.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Item not found or unable to delete"},
            status=status.HTTP_404_NOT_FOUND,
        )

    
class FileUploadView(APIView):
    serializer_class = UploadFileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FolderCreateView(APIView):
    serializer_class = CreateFolderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
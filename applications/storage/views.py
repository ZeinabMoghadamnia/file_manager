import io, os, zipfile
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, HttpResponse, JsonResponse
from django.core.paginator import Paginator

# from .models import File
from applications.storage.models import File, Folder

# from .forms import FileUploadForm
from applications.storage.forms import FileForm
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# from .serializers import FileSerializer
from applications.storage.serializers import (
    FileSerializer,
    UploadFileSerializer,
    FolderSerializer,
    CreateFolderSerializer,
    EditFileSerializer,
    EditFolderSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("storage:storage")
        else:
            return redirect("accounts:login")


class FolderAndFilesView(TemplateView):
    template_name = "storage.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_folders = Folder.objects.filter(user=self.request.user)
        user_files = File.objects.filter(user=self.request.user)

        folder_paginator = Paginator(user_folders, self.paginate_by)
        folder_page_number = self.request.GET.get("folder_page")
        folder_page_obj = folder_paginator.get_page(folder_page_number)

        file_paginator = Paginator(user_files, self.paginate_by)
        file_page_number = self.request.GET.get("file_page")
        file_page_obj = file_paginator.get_page(file_page_number)

        context["folders"] = folder_page_obj
        context["files"] = file_page_obj
        return context


class FileListView(ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        folders = Folder.objects.filter(user=request.user)
        return render(
            request, "files.html", {"files": serializer.data, "folders": folders}
        )


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

    def get_user_folders(self, user):
        return Folder.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        user_folders = self.get_user_folders(request.user)
        return render(request, "storage.html", {"folders": user_folders})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user_folders = self.get_user_folders(request.user)
            return render(request, "storage.html", {"folders": user_folders})
        return render(request, "storage.html", {"serializer": serializer})


class CreateFolderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        parent_folder_id = request.data.get("folder")

        if parent_folder_id:
            try:
                parent_folder = Folder.objects.get(pk=parent_folder_id)
            except Folder.DoesNotExist:
                return Response(
                    {"error": "Parent folder does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            parent_folder = None

        serializer = CreateFolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, parent=parent_folder)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderDetails(DetailView):
    model = Folder
    template_name = "folder_details.html"
    context_object_name = "folders"

    def post(self, request, *args, **kwargs):
        folder_id = self.kwargs["pk"]
        response = CreateFolderView.as_view()(request, pk=folder_id, user=request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder = self.get_object()
        folder_files = File.objects.filter(folder=folder)
        sub_folders = Folder.objects.filter(parent=folder)
        all_folders = Folder.objects.all()
        context["folder_files"] = folder_files
        context["sub_folders"] = sub_folders
        context["folders"] = all_folders
        context["current_folder"] = folder
        return context


class FileDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        file = get_object_or_404(File, pk=pk)
        content = file.content.read()
        content_type = file.type
        content_extension = file.content.name.split(".")[-1]
        full_content_type = f"{content_type}/{content_extension}"
        response = HttpResponse(content, content_type=full_content_type)
        return response


class DownloadFileView(View):
    def get(self, request, file_id):
        file_obj = get_object_or_404(File, pk=file_id)
        file_content = file_obj.content
        file_name_without_extension = os.path.splitext(file_obj.name)[0]
        response = FileResponse(
            file_content,
            as_attachment=True,
            filename=f"{file_name_without_extension}.{file_obj.content.name.split('.')[-1]}",
        )
        return response


class DownloadFolderView(View):
    def get(self, request, folder_id):
        folder = get_object_or_404(Folder, pk=folder_id)
        files = File.objects.filter(folder=folder)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file in files:
                file_name_without_extension = os.path.splitext(file.name)[0]
                zip_file.writestr(
                    f"{file_name_without_extension}.{file.content.name.split('.')[-1]}",
                    file.content.read(),
                )

        zip_buffer.seek(0)

        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{folder.name}.zip"'
        return response


class FileFolderSearchView(ListView):
    template_name = "search.html"
    context_object_name = "search_results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        file_results = File.objects.filter(name__icontains=query)
        folder_results = Folder.objects.filter(name__icontains=query)
        return list(file_results) + list(folder_results)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        file_results = File.objects.filter(name__icontains=query)
        folder_results = Folder.objects.filter(name__icontains=query)
        context["search_folders"] = folder_results
        context["search_files"] = file_results
        return context


class EditFileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, format=None):
        file_info = get_object_or_404(File, id=id)

        file_serializer = EditFileSerializer(file_info, data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditFolderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, format=None):
        folder_info = get_object_or_404(Folder, id=id)

        folder_serializer = EditFolderSerializer(folder_info, data=request.data)

        if folder_serializer.is_valid():
            folder_serializer.save()
            return Response(folder_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                folder_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

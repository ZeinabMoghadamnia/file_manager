from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

# from .models import File
from applications.storage.models import File

# from .forms import FileUploadForm
from applications.storage.forms import FileUploadForm
from rest_framework.permissions import AllowAny, IsAuthenticated

# from .serializers import FileSerializer
from applications.storage.serializers import FileSerializer
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


class DeleteView(APIView):
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


class FileUploadView(CreateView):
    model = File
    form_class = FileUploadForm
    template_name = "upload_file.html"
    success_url = reverse_lazy("file-list")

    def form_valid(self, form):
        # ذخیره فایل در دیتابیس
        file_instance = form.save(commit=False)
        file_instance.user = self.request.user
        file_instance.save()
        return super().form_valid(form)

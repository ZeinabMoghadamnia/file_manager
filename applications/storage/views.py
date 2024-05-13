from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import File
from .forms import FileUploadForm
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'





class FileUploadView(CreateView):
    model = File
    form_class = FileUploadForm
    template_name = 'upload_file.html'  # نام قالب برای نمایش فرم آپلود فایل
    success_url = reverse_lazy('file-list')  # مسیر پس از موفقیت آمیز بودن آپلود

    def form_valid(self, form):
        # ذخیره فایل در دیتابیس
        file_instance = form.save(commit=False)
        file_instance.user = self.request.user  # یا هرطوری که شما می‌خواهید که فایل به کاربر مربوط شود
        file_instance.save()
        return super().form_valid(form)
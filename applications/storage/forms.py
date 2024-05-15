from django import forms
from applications.storage.models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'content']
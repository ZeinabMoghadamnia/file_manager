from django import forms
from applications.storage.models import File, Folder


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["name"]

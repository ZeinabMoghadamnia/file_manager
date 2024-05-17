from django import forms
from applications.storage.models import File, Folder


class FileUploadForm(forms.ModelForm):
    folders = forms.ModelChoiceField(queryset=Folder.objects.none(), required=False)

    class Meta:
        model = File
        fields = ['name', 'content', 'folders']